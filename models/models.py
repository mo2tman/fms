# -*- coding: utf-8 -*-


from odoo import models, fields, api
from datetime import datetime, timedelta
# from dateutil.relativedelta import relativedelta

# import sys
# import sched
# import time
# import math

FMT = '%Y-%m-%d %H:%M:%S'



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
        # date = datetime.strptime(self.eta,FMT)
        # print()
        # print()
        # print(self.eta)
        # print(str(date + timedelta(hours=7)))
        # print()
        # print()
        # print()
        if self.name[:1] == 'A':
            self.planetype = 'wide'
        else:
            self.planetype = 'small'

    @api.multi
    def create_schedule(self):

        date = datetime.strptime(self.etd,FMT)
        #date_minus_three = date - timedelta(hours=3)
        schedules = self.env['fms.schedule'].search([
            ('arrival_date','=',date.date()),
             #('start_time','>=',self.date_minus_three),
            ('end_time','<=',self.etd)])
       
            
        print()
        print()
        print()
        #print(date_minus_three)
        print([schedule.flight.name for schedule in schedules])
        print()
        print()
        self.env['fms.schedule'].create({
            'flight':self.id,
            'arrival_date': date.date(),
            'start_time':date - timedelta(hours=3),
            'end_time':self.etd,
            'counter':[(6,0,[counter.id for counter in self.counters])]
            })

        self.state = 'confirmed'
###########################################
    # @api.model
    # def create(self,values):
    #     schedule = self.env['fms.schedule'].create({
    #         'date':values['eta']
    #         })
    #     return super(Flight,self).create(values)
###############################################

class Schedule(models.Model):
    _name = 'fms.schedule'

    name = fields.Char()
    counter = fields.Many2many("fms.counter")
    flight = fields.Many2one("fms.flight")
    arrival_date = fields.Date()
    start_time = fields.Datetime()
    end_time = fields.Datetime()
        



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

#   Airline = fields.One2many('airline.company','name')    

   
    # @api.one
    # def calc_age(self):
    #     date_one = fields.Date.from_string(self.birth_date)
    #     today =  fields.Date.from_string(fields.Date.today())
    #     age = relativedelta(today,date_one)
    #     self.age = age.years

    # @api.one
    # def get_manager(self):
    #   self.manager = self.department.manager.id

    # @api.multi
    # def get_emps(self):
    #   self.dep_emp = ''
    #   for emp in self.department.employees:
    #       self.dep_emp += ' ' + str(emp.name)
    #       print()
    #       print()
    #       print()
    #       print(type(self.dep_emp))
    #       print(type(emp.name))
    #       print()
    #       print()
    #       print()
    #       print()

    # @api.multi
    # def create_schedule(self):

    #     date = datetime.strptime(self.etd,FMT)
    #   #  date_minus_three = date - timedelta(hours=3)
    #     schedules = self.env['fms.schedule'].search([
    #         ('arrival_date','=',date.date()),
    #          ('start_time','>=',self.etd),
    #         ('end_time','<=',self.etd)])

    #     # counter1=[0,0,0,0,0]
    #     # for ind, val in enumerate(counter1):
    #     #     print(ind,val)

    #     print()
    #     print()
    #     print()
    #     #print(date_minus_three)
    #     print([schedule.flight.name for schedule in schedules])
    #     print()
    #     print()
    #     self.env['fms.schedule'].create({
    #         'flight':self.id,
    #         'arrival_date': date.date(),
    #         'start_time':date - timedelta(hours=3),
    #         'end_time':self.etd,
    #         'counter':[(6,0,[counter.id for counter in self.counters])]
    #         })

    #     self.state = 'confirmed'

