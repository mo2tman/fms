# -*- coding: utf-8 -*-


from odoo import models, fields, api
from datetime import datetime
# from dateutil.relativedelta import relativedelta

# import sys
# import sched
# import time
# import math


class Flight(models.Model):
    _name = 'fms.flight'

    name = fields.Char(default=" ",string="Flight Number")
    planetype = fields.Selection([('wide','Wide Body'),('small','Small Body')],default="small",compute="get_type",string="Plane Type")
    eta = fields.Datetime('Estimated Time Arrival')
    etd = fields.Datetime('Estimated Time Departure')
    route = fields.Text()
    remark = fields.Date()
    counters = fields.Many2many("fms.counter")
    state = fields.Selection([('draft','Draft'),('confirmed','Confirmed')],default='draft')

    @api.one
    def get_type(self):
        print()
        print()
        print(self.name)
        print()
        print()
        print()
        if self.name[:1] == 'A':
            self.planetype = 'wide'
        else:
            self.planetype = 'small'

    @api.multi
    def create_schedule(self):
        self.env['fms.schedule'].create({
            'flight':self.id,
            'date':self.eta
            })

        self.state = 'confirmed'

    # @api.model
    # def create(self,values):
    #     schedule = self.env['fms.schedule'].create({
    #         'date':values['eta']
    #         })
    #     return super(Flight,self).create(values)


class Schedule(models.Model):
    _name = 'fms.schedule'

    name = fields.Char()
    counter = fields.Many2many("fms.counter")
    flight = fields.Many2one("fms.flight")
    date = fields.Datetime()
        
#   Airline = fields.One2many('airline.company','name')    

   
    # @api.one
    # def calc_age(self):
    #     date_one = fields.Date.from_string(self.birth_date)
    #     today =  fields.Date.from_string(fields.Date.today())
    #     age = relativedelta(today,date_one)
    #     self.age = age.years

    # @api.one
    # def get_manager(self):
    # 	self.manager = self.department.manager.id

    # @api.multi
    # def get_emps(self):
    # 	self.dep_emp = ''
    # 	for emp in self.department.employees:
    # 		self.dep_emp += ' ' + str(emp.name)
    # 		print()
    # 		print()
    # 		print()
    # 		print(type(self.dep_emp))
    # 		print(type(emp.name))
    # 		print()
    # 		print()
    # 		print()
    # 		print()


class Type(models.Model):
    _name = 'fms.type'

    name = fields.Char()
    typecalc = fields.Char(compute='get_type')

    @api.one
    def get_type(self):
        self.typecalc = 0 if self.name[:1] == 'A' else 1


class Counter(models.Model):
    _name = 'fms.counter'

    name = fields.Char()
    available = fields.Boolean()
    ETAcoun = fields.Float('ETA')
    timenow = fields.Float(compute='get_time')
    eta = fields.Datetime()


 ########  To get current time
    @api.one
    def get_time(self):
        self.real_time_refresh()            
        self.available = True if self.timenow == self.ETAcoun else False

    @api.model
    def real_time_refresh(self):
        timeObj = fields.datetime.now()
        hour = timeObj.time().hour
        minute = timeObj.time().minute

        x = float('%s.%s' % (hour, minute if minute > 10 else '0'+ str(minute)))

        records = self.env['fms.counter'].search([])
        for record in records:
            record.timenow = x

