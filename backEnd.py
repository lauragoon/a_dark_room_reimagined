#!/usr/bin/python
# ========= HASHBANG LINE ABOVE IS MAGIC! =========
# ========= (Must be first line of file.) =========

import cgi
import cgitb
#cgitb.enable()  #diag info --- comment out once full functionality achieved

# ~~~~~~~~~~~~~~~ support functions ~~~~~~~~~~~~~~~
def FStoD():
    '''
        Converts cgi.FieldStorage() return value into a standard dictionary
        '''
    d = {}
    formData = cgi.FieldStorage()
    for k in formData.keys():
        d[k] = formData[k].value
    return d

# ~~~~~~~~~ PRE-SET VARIABLES TO MAKE THINGS EASIER ~~~~~~~~~~~~~~~

d = FStoD() # query string dictionary
forest = "" # empty b/c section is not shown until gathering wood is possible
build = ""
issue = ""
gameinD = "game" in d # T if "game" is in d; F if not
fireinD = "fire" in d # T if "fire" is in d; F if now
woodinD = "getWood" in d # T if "getWood" is in d; F if not
cartinD = "makeCart" in d #T if "makeCart" is in d; F if not
bookinD = "makeBook" in d # T if "makeBook" is in d; F if not
buildinginD = "makeBuilding" in d #T if "makeBuilding" in d; F if not
testinD = "issueTest" in d
# ~~~~~~~~~~~~~~~~~~~ GET DATA ~~~~~~~~~~~~~~~~~~~~~~

# acquire complete story text
inStream = open("story.txt", "r")
story = inStream.readlines()
inStream.close()

# acquire previous story text that has been displayed from story.txt
inDis = open("disStory.txt", "r")
disStory = inDis.read()
inDis.close()

# acquire css text for HTML formatting
inCSS = open("css.txt","r")
CSS = inCSS.read()
inCSS.close()

# acquire values of various variables from "storage.csv"
inCSV = open("storage.csv", "r")
values = inCSV.readlines()
inCSV.close()

preturns = values[0]
prestokes = values[1]
prewood = values[2]
precart = values[3]
prebooks = values[4]
prebuildings = values[5]
pretest = values[0]

preturns = preturns.split(",")[1][1:]
prestokes = prestokes.split(",")[1][1:]
prewood = prewood.split(",")[1][1:]
precart = precart.split(",")[1][1:]
prebooks = prebooks.split(",")[1][1:]
prebuildings = prebuildings.split(",")[1][1:]
pretest = pretest.split(",")[1][1:]

preturns = int(preturns.strip("\n"))
prestokes = int(prestokes.strip("\n"))
prewood = int(prewood.strip("\n"))
precart = int(precart.strip("\n"))
prebooks = int(prebooks.strip("\n"))
prebuildings = int(prebuildings.strip("\n"))
pretest = int(pretest.strip("\n"))
# ~~~~~~~~~~~~~~~~~~~~UPDATE VARIABLES ~~~~~~~~~~~~~~~~~~~~
def updateTurns(d, var):
    if gameinD:
        var = 0
    else:
        var += 1
    return var

def updateStokes(d, var):
    if gameinD:
        var = 0
    if fireinD:
        var += 1
    return var

def updateWood(d, var, cart):
    if gameinD:
        var = 5
    if fireinD and var > 0:
        var -= 1
    if woodinD:
        if cart == 1:
            var += 50
        else:
            var += 10
    if cartinD and var >= 30:
        var -= 30
    if bookinD and var >= 150:
        var -= 150
    if buildinginD and var >= 200:
        var -= 200
    return var

def updateCart(d, var, wood):
    if gameinD:
        var = 0
    elif cartinD and var == 0 and wood >= 30:
        var = 1
    return var

def updateBooks(d, var, wood):
    if gameinD:
        var = 0
    elif bookinD and wood >= 150:
        var += 1
    return var

def updateBuildings(d, var, wood, books):
    if gameinD:
        var = 0
    elif buildinginD and wood >= 200 and books >= 5:
        var += 1
    return var

def updateTest(d, var, wood, buildings, books):
    if gameinD:
        var = 0
    if testinD:
        if wood >= 500 and books >= 10 and buildings >= 5:
            var = 1
    return var

# update variables
turns = updateTurns(d, preturns)
stokes = updateStokes(d, prestokes)
cart = updateCart(d, precart, prewood)
books = updateBooks(d, prebooks, prewood)
buildings = updateBuildings(d, prebuildings, prewood, prebooks)
wood = updateWood(d, prewood, precart)
test = updateTest(d, pretest, prewood, prebuildings, prebooks)

# update HTML text for the buttons
inButtons = open("buttons.txt", "r")
buttons = inButtons.read()
inButtons.close()

# update storage.csv
def update():
    # updates values that go in storage.csv
    updateVal = "turns, " + str(turns) + "\n"
    updateVal += "stokes, " + str(stokes) + "\n"
    updateVal += "wood, " + str(wood) + "\n"
    updateVal += "cart, " + str(cart) + "\n"
    updateVal += "books, " + str(books) + "\n"
    updateVal += "buildings, " + str(buildings) +"\n"
    updateVal += "test, " + str(test) + "\n"
    # updates values in storage.csv
    outVal = open("storage.csv", 'w')
    outVal.write(updateVal)
    outVal.close()
    return updateVal

# overwrite previous csv data and show updated values
values = update()
# ~~~~~~~~~~~~~~~~~~~~GAMEPLAY~~~~~~~~~~~~~~~~~~~~~~~~
# returns default text to display after am action is selected
def actionText(d, preturns, prewood, prestokes, precart, prebooks, prebuildings):
    retStr = ""
    if preturns > 5:
        if fireinD:
            if prewood == 0:
                retStr =  "<p> <font color='gray'> not enough wood. </font> </p>"
            else:
                retStr = '''
                <p> <font color='gray'> the fire is roaring. </font> </p> \
                <p> <font color='gray'> the room is hot. </font> </p>
                '''
        if woodinD:
            retStr = '''
            <p> <font color='gray'> dry brush and dead branches <br>
            litter the forest floor. </font> </p>
            '''
        if cartinD:
            if prewood < 30:
                retStr = "<p> <font color='gray'> not enough wood. </font> </p>"
            elif precart == 0:
                retStr = '''<p> <font color='gray'>
                the rickety cart will carry <br> more wood from the forest.
                </font> </p>'''
        if bookinD:
            if prewood < 150:
                retStr = "<p> <font color='gray'> not enough wood. </font> </p>"
            else:
                retStr = '''<p> <font color='gray'>
                the book contains pages of <br> precious information that will be
                <br> passed on from generation to <br> generation.
                </font> </p>'''
        if buildinginD:
            if prewood < 200:
                retStr = "<p> <font color='gray'> not enough wood. </font> </p>"
            elif prebooks < 5:
                retStr = "<p> <font color='gray'> not enough books. </font> </p>"
            else:
                retStr = '''<p> <font color='gray'>
                a beautiful institution of knowledge <br> has been created that will
                <br> continually enrich the minds of <br> young students.
                </font> </p>'''
        if testinD:
            if prewood < 500:
                retStr = "<p> <font color='gray'> not enough wood. </font> </p>"
            elif prebooks < 10:
                retStr = "<p> <font color='gray'> not enough books. </font> </p>"
            elif prebuildings < 5:
                retStr ="<p> <font color='gray'> not enough buildings. </font> </p>"
            else:
                retStr = '''
                you have succeeded. <br>
                you look around to see the <br> haggard faces of your students. <br>
                their souls have left them <br> due to the intense exam. <br>
                you pay no attention because <br> you have found the most intelligent <br> child of your school. <br>
                Kevin Li fixes your beloved <br> spaceship in no time. <br>
                <a href="ending.html"> click here to head to your spaceship </a>
                '''
    return retStr

# HTML for inventory/storage on webpage
def inventory():
    storage = ''
    if len(values) > 2:
        storage = "<div class='storagetext'>wood</div>" + "<div class='storage'>" + str(wood) + "</div>"
    if cart > 0:
        storage += "<br><div class='storagetext'>cart</div>" + "<div class='storage'>" + str(cart) + "</div>"
    if books > 0:
        storage += "<br><div class='storagetext'>books</div>" + "<div class='storage'>" + str(books) + "</div>"
    if buildings > 0:
        storage += "<br><div class='storagetext'>buildings</div>" + "<div class='storage'>" + str(buildings) + "</div>"
    return storage

def inventoryHeight():
    height = 0
    if len(values) > 2:
        height += 30
    if (values.count(', 0') <= 2 and wood > 0) or (values.count(', 0') == 3 and wood == 0):
        height += 30
    if (values.count(', 0') <= 1 and wood > 0) or (values.count(', 0') == 2 and wood == 0):
        height += 30
    if (values.count(', 0') == 0 and wood > 0) or (values.count(', 0') == 1 and wood == 0):
        height += 30
    return str(height) + 'px;'
# ~~~~~~~~~~~~~~~~~~~~UPDATE DISPLAYED TEXT~~~~~~~~~~~~~~~~~~~~~~~~
# controls whether the forest section is seen or not
def disForest(forest, turns, d, disStort):
    # if game is restarted
    if gameinD:
        forest = ""
    if "the wood is running out." in disStory:
        forest += '''<font size="4.5"><u>A Silent Forest</u></font>
        <br><br>
        <input type="submit" class="button" name="getWood" value="gather wood">
        <br><br>
        '''
    return forest

def disBuild(disStory, cart, build):
    if gameinD:
        build = ""
    elif "make a cart" in disStory:
        if cart == 1:
            build = '''
            <form action="backEnd.py">
            <font size="3.5">build:</font> <br>
            <input type="submit" class="button" name="makeCart" value="cart" disabled >
            <span id="bookcost"><input type="submit" class="button" name="makeBook" value="book"><span style="width:80px;">150 wood</span></span>
            <span id="buildingcost"><input type="submit" id="schoolbuilding" name="makeBuilding" value="building"><span style="width:70px;">200 wood 5 books</span></span>
            <br>
            </form>'''
        else:
            build = '''
            <form action="backEnd.py">
            <font size="3.5">build:</font> <br>
            <span id="cartcost"><input type="submit" class="button" name="makeCart" value="cart"><span style="width:60px;">30 wood</span></span>
            <span id="bookcost"><input type="submit" class="button" name="makeBook" value="book"><span style="width:80px;">150 wood</span></span>
            <span id="buildingcost"><input type="submit" id="schoolbuilding" name="makeBuilding" value="building"><span style="width:70px;">200 wood 5 books</span></span>
            <br>
            </form>'''
    return build

def disIssue(disStory, issue):
    if gameinD:
        issue = ''
    elif "Important Standardized Test" in disStory:
        issue = '''
        <form action="backEnd.py">
        <font size="3.5">issue:</font> <br>
        <span id="satcost"><input type="submit" class="button" name="issueTest" value="SAT"><span style="width:69px;">500 wood 10 books 5 buildings</span></span>
        <br><br>'''
    return issue

def updateText(disStory):
    # overwrites displayed text
    outStream = open("disStory.txt", 'w')
    outStream.write(disStory)
    outStream.close()

def updateStory(d, preturns, story, disStory):
    if gameinD:
        disStory = "<p> the room is freezing. </p> \n \
        <p> the fire is dead. </p>"
    else:
        if turns < 44:
            disStory = story [turns] + disStory
        else:
            distory = ""
    return disStory

# update text on webpage
disStory =  actionText(d, preturns, prewood, prestokes, precart, prebooks,prebuildings) + updateStory(d, preturns, story, disStory)
forest = disForest(forest, turns, d, disStory)

# update disStory.txt
updateText(disStory)

# run function for build HTML section
build = disBuild(disStory, cart, build)

# update issue section's HTML
issue = disIssue(disStory, issue)
# ================== HTML STRINGS ==================
inventorycss = '''
.inventory {
    border: #000000;
    border-width: 1px;
    border-style: solid;
    width: 200px;
    height: ''' + \
    inventoryHeight() + \
    '''
    line-height: 170%;
    overflow: hidden;
}
</style>
'''

startbody = '''
<body>
<br>
<div id="left">
'''

endbody = '''
</div>
<div id="middle">
<font size="4.5"><u>A Firelit Room</u></font>
<br><br>
<form action="backEnd.py">
''' + \
buttons + build +\
"<form>" + issue + \
forest + \
"</form> " + \
'''
</div>
<div id="right">
storage
<div class="inventory">
''' + \
inventory() + \
'''
</div>
</div>
'''

# ======= Must be beginning of HTML string ========
htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!!
htmlStr += "<html><head><title> a dark room </title></head></html>\n"
htmlStr += "<html> <head>"
htmlStr += CSS
htmlStr += inventorycss
htmlStr += "</head>"
htmlStr += startbody
htmlStr += disStory
htmlStr += endbody
# debugging
#htmlStr += str(turns)
#htmlStr += str(values)
#htmlStr += str(d)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

htmlStr += "</body><html>"

print htmlStr

