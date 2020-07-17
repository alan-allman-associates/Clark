# -*- coding: utf-8 -*-
# Copyright 2020 Auguria
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import ftplib as ftp
import pysftp
import os
from os import path
from odoo import fields, models, api


class ResFTP(models.Model):
    _name = 'res.ftp'
    _description = 'FTP connections'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    url = fields.Char(string='URL')
    login = fields.Char(string='Login',)
    password = fields.Char(string='Password',)
    file_name = fields.Char(string='file name  ressouces',)
    file_name_sec = fields.Char(string='file name  missions',)
    file_source = fields.Char(string='file source simus ressources')
    file_source_sec = fields.Char(string='file source simus ressources')
    ressource_file = fields.Binary(string='FTP file')

   # @api.multi
    def sftp_access_upload(self):
        self.ensure_one()
        if self.file_name and path.exists(self.file_name):
            os.remove(self.file_name)
        if self.file_source and path.exists(self.file_source):
            os.remove(self.file_source)
        sftp = pysftp.Connection(host=self.url, username=self.login,password=self.password)
        filename=self.file_name
        file_source = self.file_source
        sftp.get(file_source, filename)
        sftp.close()
        sftp_sec = pysftp.Connection(host=self.url, username=self.login,password=self.password)
        sftp_sec.get(self.file_source_sec, self.file_name_sec)
        sftp_sec.close()
        return True

