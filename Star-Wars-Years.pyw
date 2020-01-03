from tkinter import Tk, StringVar, Label, Entry, OptionMenu, RIDGE, mainloop

master = Tk()
master.title("Star-Wars-Years")


# Calculate and Return Conversion Formulae Map
def GetFormulae(year, toBBY=True):
    # If converting from Calendar to BBY
    if toBBY:
        return {
                 "BBY": year,               # Galactic calendar Before Battle of Yavin (BBY = BBY)
                 "ABY": -year,              # Galactic calendar After Battle of Yavin (BBY = -ABY)
                 "BBE": year - 4,           # Galactic calendar Before Battle of Endor (BBY = BBE - 4)
                 "ABE": -year - 5,          # Galactic calendar After Battle of Endor (BBY = -ABE - 4)
                 "BSI": year - 34,          # Galactic calendar Before Starkiller Incident (BBY = BSI - 34)
                 "ASI": -year - 34,         # Galactic calendar After Starkiller Incident (BBY = -ASI - 34)
                 "BFE": 19 + year,          # Imperial calendar Before the Formation of the Galactic Empire (BBY = 19 + BFE)
                 "AFE": 19 - year,          # Imperial calendar After the Formation of the Galactic Empire (BBY = 19 - AFE)
                 "LY": 3277 - year,         # Lothal Calendar (BBY = 3277 - LY)
                 "C.R.C.": 7977 - year,     # Hosnian Reckoning (BBY = 7977 - C.R.C.)
                 "YK": 867 - year           # Naboo calendar Year of Kwilaan (BBY = 867 - YK)
               }
    # Otherwise, if converting from BBY to Calendars
    else:
        return {
                 "BBY": year,               # Galactic calendar Before Battle of Yavin (BBY = BBY)
                 "ABY": -year,              # Galactic calendar After Battle of Yavin (ABY = -BBY)
                 "BBE": 4 + year,           # Galactic calendar Before Battle of Endor (BBE = 4 + BBY)
                 "ABE": -year - 4,          # Galactic calendar After Battle of Endor (ABE = -BBY - 4)
                 "BSI": 34 + year,          # Galactic calendar Before Starkiller Incident (BSI = 34 + BBY)
                 "ASI": -year - 34,         # Galactic calendar After Starkiller Incident (ASI = -BBY - 34)
                 "BFE": year - 19,          # Imperial calendar Before the Formation of the Galactic Empire (BFE = BBY - 19)
                 "AFE": 19 - year,          # Imperial calendar After the Formation of the Galactic Empire (AFE = 19 - BBY)
                 "LY": 3277 - year,         # Lothal Calendar (LY = 3277 - BBY)
                 "C.R.C.": 7977 - year,     # Hosnian Reckoning (C.R.C. = 7977 - BBY)
                 "YK": 867 - year           # Naboo calendar Year of Kwilaan (YK = 867 - BBY)
               }


# Calculate Year in BBY
def ConvertToBBY(year, menu):
    return GetFormulae(year)[menu.calendarValue.get()]


# Convert Calendars
def Convert(year):
    # Get Year in BBY
    yearBBY = ConvertToBBY(year, ConversionCalendar)
    # Get Conversion Formulae Map from BBY to Year
    fromBBYMap = GetFormulae(yearBBY, False)
    # Display calcluated values
    for calendar in Calendars:
        try:
            calendar.yearLabel["text"] = str(fromBBYMap[calendar.calendarLabel["text"]])
        except KeyError:
            pass

# List of Calendars
CalendarList = list(GetFormulae(0).keys())
# Default Calendar
DefaultCalendar = CalendarList[0]

# UserCalendar Class
class UserCalendar(object):
    def __init__(self, rowValue=1, columnValue=0, yearWidthValue=20, calendarWidthValue=14):
        # Member variable that represents the year value
        self.yearValue = StringVar(master)
        # Textbox entry for user input of year value
        self.yearEntry = Entry(master, textvariable=self.yearValue, bg='gray88', justify='center', width=yearWidthValue)
        self.yearEntry.grid(row=rowValue, column=columnValue, ipady=3)

        # Member variable that represents the associated calendar
        self.calendarValue = StringVar(master)
        self.calendarValue.set(DefaultCalendar)
        # Drop-down menu for user input of associated calendar
        self.calendarMenu = OptionMenu(master, self.calendarValue, *GetFormulae(0).keys())
        self.calendarMenu.config(width=calendarWidthValue)
        self.calendarMenu.grid(row=rowValue, column=columnValue + 1)

# Calendar Class
class Calendar(object):
    def __init__(self, calendarValue, rowValue=2, columnValue=0, yearWidthValue=17, calendarWidthValue=17):
        # Label for displaying year value
        self.yearLabel = Label(master, text="", relief=RIDGE, width=yearWidthValue, height=1)
        self.yearLabel.grid(row=rowValue, column=columnValue)

        # Label for associated calendar
        self.calendarLabel = Label(master, text=calendarValue, relief=RIDGE, width=calendarWidthValue, height=1)
        self.calendarLabel.grid(row=rowValue, column=columnValue + 1)


# Purpose: Validate player entered integer, valid equation, or 'x' cancel
# Parameters: User input (string)
# Returns: Converted user input (integer) or raw user input (string), validity (boolean)
def Validate(userInput):
    # Remove all whitespace
    userInput = ("".join(userInput.split())).lower()
    # Ensure input is not empty string or 'x' cancel
    if userInput != "" and userInput != "x":
        # Remove all thousand-separator commas
        userInput = userInput.replace(",", "")
        # Replace all 'x' characters with multiplication operator
        userInput = userInput.replace("x", "*")
        # Check if input is integer
        try:
            # Valid integer
            return int(userInput), True
        except:
            # Check if input is valid equation
            for char in userInput:
                # Valid equations only contain digits, arithmetic operators, or decimal point
                if char not in "0123456789+-*/.":
                    return userInput, False
            try:
                # Valid equation
                return int(eval(userInput)), True
            except:
                # Catch-all of remaining possible invalid input
                return userInput, False
    # Empty string and 'x' cancel are not valid integers
    return userInput, False


# Conversion Table
def ConvertCalendars():
    testedInput = Validate(ConversionCalendar.yearValue.get())
    if testedInput[1]:
        Convert(testedInput[0])
    else:
        for calendar in Calendars:
            calendar.yearLabel["text"] = ""

# Conversion Prompt Label
ConversionPrompt = Label(master, text="Type the year value and select the associated calendar\nto solve for all the calendars.")
ConversionPrompt.grid(row=0, column=0, columnspan=2)

# Conversion User Input
ConversionCalendar = UserCalendar()
ConversionCalendar.yearValue.trace('w', lambda *pargs: ConvertCalendars())
ConversionCalendar.calendarValue.trace('w', lambda *pargs: ConvertCalendars())
ConversionCalendar.yearEntry.focus()

# Calendar Instance List
Calendars = []

# Generate Calendar Instances List
for index, element in enumerate(CalendarList, start=2):
    # Start at row 2
    Calendars.append(Calendar(CalendarList[index - 2], index))


# Duration Solver
def CalculateDuration():
    testedStartInput = Validate(StartCalendar.yearValue.get())
    testedEndInput = Validate(EndCalendar.yearValue.get())
    if testedStartInput[1] and testedEndInput[1]:
        startBBY = ConvertToBBY(testedStartInput[0], StartCalendar)
        endBBY = ConvertToBBY(testedEndInput[0], EndCalendar)
        diffBBY = startBBY - endBBY
        DurationResult.yearLabel["text"] = str(diffBBY - 1) + " or " + str(diffBBY)
    else:
        DurationResult.yearLabel["text"] = ""

# Duration Prompt Label
DurationPrompt = Label(master, text="Type the year value and select the associated calendar\nfor the start and end to solve for the age.")
DurationPrompt.grid(row=0, column=2, columnspan=2)

# Start User Input
StartLabel = Label(master, text="Start Year:", relief=RIDGE, width=39, height=1)
StartLabel.grid(row=1, column=2, columnspan=2)
StartCalendar = UserCalendar(2, 2)
StartCalendar.yearValue.trace('w', lambda *pargs: CalculateDuration())
StartCalendar.calendarValue.trace('w', lambda *pargs: CalculateDuration())

# End User Input
StartLabel = Label(master, text="End Year:", relief=RIDGE, width=39, height=1)
StartLabel.grid(row=3, column=2, columnspan=2)
EndCalendar = UserCalendar(4, 2)
EndCalendar.yearValue.trace('w', lambda *pargs: CalculateDuration())
EndCalendar.calendarValue.trace('w', lambda *pargs: CalculateDuration())

# Duration Result
DurationLabel = Label(master, text="Resulting Age", relief=RIDGE, width=39, height=1)
DurationLabel.grid(row=5, column=2, columnspan=2)
DurationResult = Calendar("Galactic Standard Years", 6, 2, 17, 19)

mainloop()
