# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida-core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
"""Plugin for transport over SSH (and SFTP for file transfer). Modified to make it work with ARCHER2"""
# pylint: disable=too-many-lines
from binascii import hexlify
import os

from paramiko.agent import Agent
from paramiko.common import DEBUG
from paramiko.dsskey import DSSKey
from paramiko.ecdsakey import ECDSAKey
from paramiko.ed25519key import Ed25519Key
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import (
    SSHException,
)
from paramiko import SSHClient

from aiida.transports.plugins.ssh import SshTransport as StockSshTransport

__all__ = ('SshTransport', 'SSHTransport4C')


class Archer2SSHClient(SSHClient):
    """
    Specialised SSHClient for ARCHER2
    """
    def _auth(
        self,
        username,
        password,
        pkey,
        key_filenames,
        allow_agent,
        look_for_keys,
        gss_auth,
        gss_kex,
        gss_deleg_creds,
        gss_host,
        passphrase,
    ):
        """
        Try, in order:

            - Plain username/password auth, if a password was given.
            - A series of trials using public keys 

        """
        saved_exception = None
        allowed_types = set()
        if passphrase is None and password is not None:
            passphrase = password


        if pkey is not None:
            try:
                self._log(
                    DEBUG,
                    "Trying SSH key {}".format(
                        hexlify(pkey.get_fingerprint())
                    ),
                )
                allowed_types = self._transport.auth_publickey(username, pkey)
                if not allowed_types:
                    return
            except SSHException as e:
                saved_exception = e


        # Using supplied file path
        for key_filename in key_filenames:
            for pkey_class in (RSAKey, DSSKey, ECDSAKey, Ed25519Key):
                try:
                    key = self._key_from_filepath(
                        key_filename, pkey_class, passphrase
                    )
                    allowed_types = self._transport.auth_publickey(username, key)
                    if not allowed_types:
                        return
                    break
                except SSHException as e:
                    saved_exception = e

        # Try default ssh key in ~/.ssh 
        keyfiles = []
        for keytype, name in [
            (DSSKey, "dsa"),
            (ECDSAKey, "ecdsa"),
            (Ed25519Key, "ed25519"),
        ]:
            # ~/ssh/ is for windows
            for directory in [".ssh", "ssh"]:
                full_path = os.path.expanduser(
                    "~/{}/id_{}".format(directory, name)
                )
                if os.path.isfile(full_path):
                    # TODO: only do this append if below did not run
                    keyfiles.append((keytype, full_path))
                    if os.path.isfile(full_path + "-cert.pub"):
                        keyfiles.append((keytype, full_path + "-cert.pub"))

            if not look_for_keys:
                keyfiles = []

            for pkey_class, filename in keyfiles:
                try:
                    key = self._key_from_filepath(
                        filename, pkey_class, passphrase
                    )
                    # for 2-factor auth a successfully auth'd key will result
                    # in ['password']
                    allowed_types = self._transport.auth_publickey(username, key)
                    if not allowed_types:
                        return
                    break
                except (SSHException, IOError) as e:
                    saved_exception = e

        # Try using agents
        if self._agent is None:
            self._agent = Agent()

        for key in self._agent.get_keys():
            try:
                id_ = hexlify(key.get_fingerprint())
                self._log(DEBUG, "Trying SSH agent key {}".format(id_))
                # for 2-factor auth a successfully auth'd key password
                # will return an allowed 2fac auth method
                allowed_types = self._transport.auth_publickey(username, key)
                if not allowed_types:
                    return
                break
            except SSHException as e:
                saved_exception = e

        # Password authentication goes last
        try:
            allowed_types = set( self._transport.auth_password(username, password))
        except SSHException as e:
            saved_exception = e

        # If allowed_types is empty the authentication worked
        if not allowed_types:
            return 

         # if we got an auth-failed exception earlier, re-raise it
        if saved_exception is not None:
            raise saved_exception

       
        raise SSHException("No authentication methods available")

class ARCHER24CSSHClient(SSHClient):
    """
    Client for the 4-cabinet service

    ARCHER2 (4-cabint pilot system) uses a unusual authentication order such as the password is attempted
    first, followed by the public key. Hence we have to override the _auth method for it to work.
    """
    
    def _auth(
        self,
        username,
        password,
        pkey,
        key_filenames,
        allow_agent,
        look_for_keys,
        gss_auth,
        gss_kex,
        gss_deleg_creds,
        gss_host,
        passphrase,
    ):
        """
        Try, in order:

            - Plain username/password auth, if a password was given.
            - A series of trials using public keys 

        """
        saved_exception = None
        allowed_types = set()
        if passphrase is None and password is not None:
            passphrase = password

        # Password authentication goes first
        try:
            allowed_types = set( self._transport.auth_password(username, password))
        except SSHException as e:
            saved_exception = e

        if pkey is not None:
            try:
                self._log(
                    DEBUG,
                    "Trying SSH key {}".format(
                        hexlify(pkey.get_fingerprint())
                    ),
                )
                allowed_types = self._transport.auth_publickey(username, pkey)
                if not allowed_types:
                    return
            except SSHException as e:
                saved_exception = e


        # Using supplied file path
        for key_filename in key_filenames:
            for pkey_class in (RSAKey, DSSKey, ECDSAKey, Ed25519Key):
                try:
                    key = self._key_from_filepath(
                        key_filename, pkey_class, passphrase
                    )
                    allowed_types = self._transport.auth_publickey(username, key)
                    if not allowed_types:
                        return
                    break
                except SSHException as e:
                    saved_exception = e

        # Try default ssh key in ~/.ssh 
        keyfiles = []
        for keytype, name in [
            (DSSKey, "dsa"),
            (ECDSAKey, "ecdsa"),
            (Ed25519Key, "ed25519"),
        ]:
            # ~/ssh/ is for windows
            for directory in [".ssh", "ssh"]:
                full_path = os.path.expanduser(
                    "~/{}/id_{}".format(directory, name)
                )
                if os.path.isfile(full_path):
                    # TODO: only do this append if below did not run
                    keyfiles.append((keytype, full_path))
                    if os.path.isfile(full_path + "-cert.pub"):
                        keyfiles.append((keytype, full_path + "-cert.pub"))

            if not look_for_keys:
                keyfiles = []

            for pkey_class, filename in keyfiles:
                try:
                    key = self._key_from_filepath(
                        filename, pkey_class, passphrase
                    )
                    # for 2-factor auth a successfully auth'd key will result
                    # in ['password']
                    allowed_types = self._transport.auth_publickey(username, key)
                    if not allowed_types:
                        return
                    break
                except (SSHException, IOError) as e:
                    saved_exception = e

        # Try using agents
        if self._agent is None:
            self._agent = Agent()

        for key in self._agent.get_keys():
            try:
                id_ = hexlify(key.get_fingerprint())
                self._log(DEBUG, "Trying SSH agent key {}".format(id_))
                # for 2-factor auth a successfully auth'd key password
                # will return an allowed 2fac auth method
                allowed_types = self._transport.auth_publickey(username, key)
                if not allowed_types:
                    return
                break
            except SSHException as e:
                saved_exception = e

        # If allowed_types is empty the authentication worked
        if not allowed_types:
            return 

         # if we got an auth-failed exception earlier, re-raise it
        if saved_exception is not None:
            raise saved_exception

       
        raise SSHException("No authentication methods available")


class SshTransport(StockSshTransport):  # pylint: disable=too-many-public-methods
    """
    Support connection, command execution and data transfer to remote computers via SSH+SFTP.
    """
    # Valid keywords accepted by the connect method of paramiko.SSHClient
    # I disable 'password' and 'pkey' to avoid these data to get logged in the
    # aiida log file.
    CLIENT_CLASS = Archer2SSHClient
    def __init__(self, *args, **kwargs):
        """
        Initialize the SshTransport class.

        :param machine: the machine to connect to
        :param load_system_host_keys: (optional, default False)
           if False, do not load the system host keys
        :param key_policy: (optional, default = paramiko.RejectPolicy())
           the policy to use for unknown keys

        Other parameters valid for the ssh connect function (see the
        self._valid_connect_params list) are passed to the connect
        function (as port, username, password, ...); taken from the
        accepted paramiko.SSHClient.connect() params.
        """
        import paramiko
        super().__init__(*args, **kwargs)

        self._sftp = None
        self._proxy = None

        self._machine = kwargs.pop('machine')

        self._client = self.CLIENT_CLASS() 
        self._load_system_host_keys = kwargs.pop('load_system_host_keys', False)
        if self._load_system_host_keys:
            self._client.load_system_host_keys()

        self._missing_key_policy = kwargs.pop('key_policy', 'RejectPolicy')  # This is paramiko default
        if self._missing_key_policy == 'RejectPolicy':
            self._client.set_missing_host_key_policy(paramiko.RejectPolicy())
        elif self._missing_key_policy == 'WarningPolicy':
            self._client.set_missing_host_key_policy(paramiko.WarningPolicy())
        elif self._missing_key_policy == 'AutoAddPolicy':
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        else:
            raise ValueError(
                'Unknown value of the key policy, allowed values '
                'are: RejectPolicy, WarningPolicy, AutoAddPolicy'
            )

        self._connect_args = {}
        for k in self._valid_connect_params:
            try:
                self._connect_args[k] = kwargs.pop(k)
            except KeyError:
                pass

        # Additional password is needed for ARCHER
        if 'archer2' in self._machine:
            username = self._connect_args['username'].upper()
            env_name = 'ARCHER2_PASS_' + username
            password = os.environ.get(env_name)
            
            if not password:
                # Fallback for generic ones
                password = os.environ.get('ARCHER2_PASS')

            if not password:
                raise ValueError(f'Cannot found password for ARCHER2 - please set the {env_name} environmental variable')
            self._connect_args['password'] = password


class SshTransport4C(SshTransport):
    """
    SSH Transport for the 4 cabinet service
    """
    CLIENT_CLASS = ARCHER24CSSHClient