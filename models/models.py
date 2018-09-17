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

    name = fields.Char(string="Flight Number")
    planetype = fields.Selection([('wide','Wide Body'),('small','Small Body')],default="small",compute="get_type",string="Plane Type",store=True)
    eta = fields.Datetime('Estimated Time Arrival')
    etd = fields.Datetime('Estimated Time Departure')
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    route = fields.Text()
    remark = fields.Date()
    counter = fields.Char()
    state = fields.Selection([('draft','Draft'),('confirmed','Confirmed')],default='draft')
    stand = fields.Char()

    @api.one
    def get_type(self):
        # date = datetime.strptime(self.eta,FMT)
        if self.name[:1] == 'A':
            self.planetype = 'wide'
        else:
            self.planetype = 'small'
        print()
        print()
        print()
        print(self.name)
        print(self.planetype)
        print()
        print()
        print()

    @api.multi
    def create_schedule(self):
        counter = '0'
        stand = '0'
        counter_found = False
        stand_found = False

        date_dep = datetime.strptime(self.etd,FMT)
        date_arr = datetime.strptime(self.eta,FMT)
        date_minus_three = date_dep - timedelta(hours=3)
        date_plus_two = date_arr + timedelta(hours=2)
        self.start_time = date_minus_three
        self.end_time = date_plus_two


        for i in range(1,8):
            schedules = self.env['fms.schedule'].search(['&','&',
                ('arrival_date','=',date_dep.date()),
                ('counter','=',i),'|','&',
                ('counter_start_time','<=',self.start_time),
                ('counter_end_time','>=',self.start_time),'&',
                ('counter_start_time','<=',self.etd),
                ('counter_end_time','>=',self.etd)])
            print()
            print()
            print()
            print(i)
            print([schedule.flight.name for schedule in schedules])
            print()
            print()
            print()
            print()

            if len(schedules) == 0:
                print(True)
                counter_found = True
                counter = str(i)
                break
            else: print(False)
        print(counter)


        loop_total = 0
        loop_total = 4 if self.planetype == 'wide' else  44
        for i in range(1,loop_total):
            schedules = self.env['fms.schedule'].search(['&','&',
                ('arrival_date','=',date_arr.date()),
                ('stand','=',i),'|','&',
                ('stand_start_time','<=',self.eta),
                ('stand_end_time','>=',self.eta),'&',
                ('stand_start_time','<=',self.end_time),
                ('stand_end_time','>=',self.end_time),
                ('planetype','=',self.planetype)])
            print()
            print()
            print()
            print(i)
            print([schedule.flight.name for schedule in schedules])
            print()
            print()
            print()
            print()

            if len(schedules) == 0:
                print(True)
                stand_found = True
                stand = str(i)
                break
            else: print(False)
        print(stand)
       
            
        if counter_found and stand_found: 
            self.env['fms.schedule'].create({
                'flight':self.id,
                'arrival_date': date_dep.date(),
                'counter_start_time':date_minus_three,
                'stand_start_time':self.eta,
                'counter_end_time':self.etd,
                'stand_end_time':date_plus_two,
                'counter': counter,
                'stand': stand
                # [(6,0,[counter.id for counter in self.counters])]
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
    counter = fields.Char()
    flight = fields.Many2one("fms.flight")
    arrival_date = fields.Date()
    counter_start_time = fields.Datetime()
    stand_start_time = fields.Datetime()
    counter_end_time = fields.Datetime()
    stand_end_time = fields.Datetime()
    stand = fields.Char()
    planetype = fields.Selection([('wide','Wide Body'),('small','Small Body')],related="flight.planetype")

    @api.one
    def printing(self):
        print()
        print()
        print()
        print(self.end_time)
        print()
        print()
        print()
        



# class Type(models.Model):
#     _name = 'fms.type'

#     name = fields.Char()
#     typecalc = fields.Char(compute='get_type')

#     @api.one
#     def get_type(self):
#         self.typecalc = 0 if self.name[:1] == 'A' else 1


# class Counter(models.Model):
#     _name = 'fms.counter'

#     name = fields.Char()
#     available = fields.Boolean()
#     ETAcoun = fields.Float('ETA')
#     timenow = fields.Float(compute='get_time')
#     eta = fields.Datetime()


#  ########  To get current time
#     @api.one
#     def get_time(self):
#         self.real_time_refresh()            
#         self.available = True if self.timenow == self.ETAcoun else False

#     @api.model
#     def real_time_refresh(self):
#         timeObj = fields.datetime.now()
#         hour = timeObj.time().hour
#         minute = timeObj.time().minute

#         x = float('%s.%s' % (hour, minute if minute > 10 else '0'+ str(minute)))

#         records = self.env['fms.counter'].search([])
#         for record in records:
#             record.timenow = x

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

