import requests
from datetime import date

def get_url(year):
    return f"https://nolaborables.com.ar/api/v2/feriados/{year}"

months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
days = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

def day_of_week(day, month, year):
    return days[date(year, month, day).weekday()]

class NextHoliday:
    def __init__(self):
        self.loading = True
        self.year = date.today().year
        self.holiday = None

    def set_next(self, holidays, type):
        now = date.today()
        today = {
            'day': now.day,
            'month': now.month
        }
        
        if type == None:
            holiday = next(
                (h for h in holidays if h['mes'] == today['month'] and h['dia'] > today['day'] or h['mes'] > today['month']),
                holidays[0]
            )
        else:
            holiday = next(
                (h for h in holidays if h['tipo'] == type and h['mes'] == today['month'] and h['dia'] > today['day'] or h['mes'] > today['month'] and h['tipo'] == type),
                {"error": f"No se encuentra ningun feriado de tipo: {type}"}
            )
        
        self.loading = False
        self.holiday = holiday

    def fetch_holidays(self,type=None):
        response = requests.get(get_url(self.year))
        data = response.json()  
        self.set_next(data, type)

    def render(self):
        if self.loading:
            print("Buscando...")
        else:
            if(len(self.holiday.keys()) == 1):
                print(self.holiday["error"])
                return
            print("Próximo feriado")
            print(self.holiday['motivo'])
            print("Fecha:")
            print(day_of_week(self.holiday['dia'], self.holiday['mes'] , self.year))
            print(self.holiday['dia'])
            print(months[self.holiday['mes'] - 1])
            print("Tipo:")
            print(self.holiday['tipo'])

#next_holiday = NextHoliday()
#next_holiday.fetch_holidays("puente")
#next_holiday.render()
