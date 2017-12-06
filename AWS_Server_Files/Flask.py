from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__, template_folder=".")
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAuEnMWulx3DRE9n7Jtgf_FduFrIodAYsw"
GoogleMaps(app)

#make circles list
colorscale={0:"#FFFFFF",
           1:"#FFFFFF",   #white
           2:"#FF8888",
           3:"#FF6666",
           4:"#FF4444",   #pink
           5:"#FF2222",
           6:"#FF0000",   #red
           7:"#DD0000",
           8:"#BB0000",
           9:"#990000",
           10:"#660000",   #maroon
           11:"#00FF00"
    }

def findroughcolor(c):
    c=int(c)
    return colorscale.get(c,"00FF00")

iconpaths={0:"/static/mapicons/greendot12px.png",
           1:"/static/mapicons/greendot12px.png", 
           2:"/static/mapicons/greendot12px.png",
           3:"/static/mapicons/greendot12px.png",
           4:"/static/mapicons/greendot12px.png",
           5:"/static/mapicons/yellowdot12px.png",
           6:"/static/mapicons/yellowdot12px.png",
           7:"/static/mapicons/yellowdot12px.png",
           8:"/static/mapicons/reddot12px.png",
           9:"/static/mapicons/reddot12px.png",
           10:"/static/mapicons/reddot12px.png",
          }   
def deticon(c):
    c=int(c)
    return iconpaths.get(c,"/static/mapicons/greendot12px.png")

#set1=[[37.4500,-122.1350,6],[37.4400,-122.1350,8],[37.4300,-122.1350,10]]    
 
#create map objects for Flask framework(Google API) 
@app.route('/')
def mapview():
    centercoord=[37.337361,-121.882691]
    
    #parse trigger data from MainTrigger.txt
    path = "MainTrigger.txt"
    set0=[]
    n=[]
    with open(path,'r') as f:
        for line in f:
            n=line.split()
            n[0]=float(n[0])
            n[1]=float(n[1])
            set0.append(n)

    m0=[]
    m1=[]
    #build marker dictionaries
    for i in range(len(set0)):
        imgpath="<img src=\"/static/images/"+set0[i][3]+"\" width=100px/>"
        m0.append({'lat':set0[i][0],'lng':set0[i][1],'infobox':imgpath})
        m1.append({'lat':set0[i][0],'lng':set0[i][1]})
    
    #set default circle settings on map
    label2=['stroke_color','stroke_opacity','stroke_weight','fill_color','fill_opacity','center','radius']
    c1=[]
    S_O1=1.0 #stroke opacity
    S_W1=1 #stroke weight
    F_O1=.6 #fill opacity
    RAD1=7 #radius
    templist=[0,S_O1,S_W1,0,F_O1,0,RAD1]
    
    #build required circle dictionaries
    for i in range(len(set0)):
        color = findroughcolor(set0[i][2])
        templist[0]=color #stroke_color
        templist[3]=color #fill_color
        templist[5]=m1[i] #center  
        c1.append(dict(zip(label2,templist)))
    
    #create Map object
    mymap = Map(
        identifier = "potholemap",
        varname="potholemap",
        lat=centercoord[0], lng=centercoord[1],
        circles=c1,
	    markers=m0,
	    zoom=16,
	    cluster=False,
        style=("height:750px;" "width:80%;" "position:relative;")
	)
    
    #parse Roughness data
    path = "MainRoughness.txt"
    set1=[]
    n=[]
    with open(path,'r') as f:
        for line in f:
            n=line.split()
            n[0]=float(n[0])
            n[1]=float(n[1])
            set1.append(n)

    m2=[]
    #build second set of marker dictionaries
    for i in range(len(set1)):
        iconpath=deticon(set1[i][2])
        m2.append({'lat':set1[i][0],'lng':set1[i][1],'icon':iconpath})
        
     #generate roughness map object   
    sndmap = Map(
        identifier = "roughmap",
        varname="roughmap",
        lat=centercoord[0], lng=centercoord[1],
        #circles=c1,
		markers=m2,
		zoom=16,
        cluster=False,
        style=("height:750px;" "width:80%;" "position:relative;")
        )

    return render_template('htmlcode.html', mymap=mymap, sndmap=sndmap) #utilize htmlcode.html as template for website

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=8000) #run in debug mode (site actually utilizes nohup command will not see debug messeges)
