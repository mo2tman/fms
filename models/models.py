# -*- coding: utf-8 -*-


from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


FMT = '%Y-%m-%d %H:%M:%S' #Python format of date and time



class Flight(models.Model): 
    _name = 'fms.flight'

    name = fields.Char(string="Flight Number")
    planetype = fields.Selection([('wide','Wide Body'),('small','Small Body')],default="small",compute="get_type",string="Plane Type")
    eta = fields.Datetime('Estimated Time Arrival')
    etd = fields.Datetime('Estimated Time Departure')
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    Route = fields.Text(string="Route")
    counter = fields.Char()
    state = fields.Selection([('draft','Draft'),('confirmed','Confirmed')],default='draft')
    stand = fields.Char()
    ata = fields.Datetime('Actual Time Arrival')
    atd = fields.Datetime('Actual Time Departure')
    arrived = fields.Boolean()
    arrival = fields.Selection([('late','Late'),('on_time','On Time')])
    departure = fields.Selection([('late','Late'),('on_time','On Time')])
    airline = fields.Many2one('fms.airline')


    @api.onchange('eta','etd') #function to give a default values foe ata and atd equals to the e
    def set_actual(self):
        self.ata = self.eta
        self.atd = self.etd

    @api.one
    def flight_performance(self):
        eta = datetime.strptime(self.eta,FMT)
        etd = datetime.strptime(self.etd,FMT)
        ata = datetime.strptime(self.ata,FMT)
        atd = datetime.strptime(self.atd,FMT)
        arr_result = (ata - eta).seconds / 60
        dep_result = (atd - etd).seconds / 60

        if arr_result > 30: #the airport tolarnce is 30 mins
            self.arrival = 'late'
        else:
            self.arrival = 'on_time'

        if dep_result > 30:
            self.departure = 'late'
        else:
            self.departure = 'on_time'




    @api.one
    def get_type(self): #to get the type
        if self.name[:1] == 'A':
            self.planetype = 'wide'
            print() 
            print()
            print()
            print()
            print(self.planetype)
            print()
            print()
            print()
            print()
            print()
        else:
            self.planetype = 'small'

             
            print()
            print()
            print()
            print()
            print(self.planetype)
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
                ('counter_end_time','>=',self.etd)]) #polish notation to or/and the condition
         
            if len(schedules) == 0:
                print(True)
                counter_found = True
                counter = str(i)
                break

        if not counter_found: 
            raise ValidationError('No Counter Found')
            return
        print(counter)


        loop_total = 0
        loop_total = 3 if self.planetype == 'wide' else  44
        for i in range(1,loop_total):
            schedules = self.env['fms.schedule'].search(['&','&',
                ('arrival_date','=',date_arr.date()),
                ('stand','=',i),'|','&',
                ('stand_start_time','<=',self.eta),
                ('stand_end_time','>=',self.eta),'&',
                ('stand_start_time','<=',self.end_time),
                ('stand_end_time','>=',self.end_time),
                ('planetype','=',self.planetype)])
          

            if len(schedules) == 0:
                print(True)
                stand_found = True
                stand = str(i)
                break
        if not stand_found: 
            raise ValidationError('No Stand Found')
            return
        print(stand)
       
            
        if counter_found and stand_found: 
            self.env['fms.schedule'].create({
                'flight':self.id,
                'arrival_date': date_dep.date(),
                'arrival_date': self.eta,
                'counter_start_time':date_minus_three,
                'stand_start_time':self.eta,
                'counter_end_time':self.etd,
                'stand_end_time':date_plus_two,
                'counter': counter,
                'stand': stand
                })

        self.state = 'confirmed'


class Schedule(models.Model):
    _name = 'fms.schedule'

    name = fields.Char()
    counter = fields.Char()
    flight = fields.Many2one("fms.flight")
    arrival_date = fields.Date()
    arrival_time = fields.Datetime()
    counter_start_time = fields.Datetime()
    stand_start_time = fields.Datetime()
    counter_end_time = fields.Datetime()
    stand_end_time = fields.Datetime()
    stand = fields.Char()
    planetype = fields.Selection([('wide','Wide Body'),('small','Small Body')],related="flight.planetype")

        


class Airline(models.Model):
    _name = 'fms.airline'

    name = fields.Char()


class Perfomance(models.TransientModel):
    _name='fms.performance'

    airline = fields.Many2one('fms.airline')
    arrival_date = fields.Date()
    flights = fields.Many2many('fms.flight',compute="get_flights")
    no_flights = fields.Integer(compute="get_flights")
    late_arrival = fields.Integer(compute="get_flights")
    late_departure = fields.Integer(compute="get_flights")
    performance = fields.Float(compute="get_flights")
    start_date = fields.Date()
    end_date = fields.Date()

    @api.one
    def get_flights(self): 
        self.flights = self.env['fms.flight'].search([('airline','=',self.airline.id)
            ,('ata','>=',self.start_date),('ata','<=',self.end_date)])

        self.no_flights = len(self.flights)
        late_arrival = 0 
        late_departure = 0 
        for flight in self.flights:
            if flight.arrival == 'late':
                late_arrival += 1

            if flight.departure == 'late':
                late_departure += 1

        self.late_arrival = late_arrival
        self.late_departure = late_departure

        self.performance = (1 - (late_arrival + late_departure ) / self.no_flights) * 100


        
   