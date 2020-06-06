import os
import colorama
import random
import time
import lista
try:
    import msvcrt
except:
    import sys
    import select
    import tty
    import termios
    fd=sys.stdin.fileno()
    oldterm=termios.tcgetattr(fd)

def clear():
    if os.name == 'nt':
        os.system('cls')
    else: 
        os.system('clear')

def kbhit():
    if os.name == "nt":
        return msvcrt.kbhit()
    else:
        try:
          tty.setcbreak(sys.stdin.fileno(),when=termios.TCSANOW)
          return select.select([sys.stdin], [], [], 0) != ([], [], [])
        finally:
          termios.tcsetattr(fd, termios.TCSADRAIN, oldterm)

def kbget():
    if os.name == "nt":
        return msvcrt.getwche()
    else:
        return sys.stdin.read(1)[0]

def ahorcado(error):
    col=getattr(colorama.Fore, "GREEN")
    a="  _____"
    b=" |     "
    c=" |    "
    d=" |    "
    e="_|_"
    if error>=1:
        b+="O"
    if error>=2:
        c+=" |"
    if error>=3:
        col=getattr(colorama.Fore, "YELLOW")
        c=c[:6]
        c+="/|"
    if error>=4:
        c+="\\"
    if error>=5:
        col=getattr(colorama.Fore, "RED")
        d+="/"
    if error>=6:
        d+=" \\"
        time.sleep(0.5)
        clear()
        b=b[:6]+"\\O/"
        c=c[:6]+" |"
        print(col,a,"\n",b,"\n",c,"\n",d,"\n",e,"\n\n¡Perdiste!",colorama.Style.RESET_ALL)
        time.sleep(0.5)
        clear()
        b=b[:6]+" O"
        c=c[:6]+"/|\\"
    print(col,a,"\n",b,"\n",c,"\n",d,"\n",e,colorama.Style.RESET_ALL)

def ganador():
    a="       "
    b=" |     "
    c=" |    "
    d=" |    "
    e="_|_"
    s=""
    if len(LetrasUsadas)!=1:
        s="s"
    for i in range(4):
        clear()
        col = getattr(colorama.Fore, "GREEN")
        pos1 = c+"  O"
        pos2 = d+" /|\\"
        pos3 = e+"    / \\"
        print(col, a, "\n", b, "\n", pos1, "\n", pos2, "\n", pos3, colorama.Style.RESET_ALL,"\n"+str(lineas),"\n\n¡Felicidades, ganaste en", len(LetrasUsadas), "intento"+str(s)+"!")
        time.sleep(0.5)
        clear()
        pos1 = b+"\\O/"
        pos2 = c+"  |"
        pos3 = d+" / \\"
        print(col, a, "\n", pos1, "\n", pos2, "\n", pos3,"\n",e, colorama.Style.RESET_ALL,"\n"+str(lineas),"\n\n¡Felicidades, ganaste en", len(LetrasUsadas), "intento"+str(s)+"!")
        time.sleep(0.5)

def agregar(partida):
    f=open("partidas","a+")
    f.write(partida[0]+" | "+str(partida[1])+" | "+str(partida[2])+" | "+partida[3]+"\n")
    f.close()

def top5():
    partidas = []
    arch = open("partidas", "r")
    for p in arch:
        partidas.append(p.replace("\n", "").split("|"))
    partidas = sorted(partidas, key=lambda x: int(x[1])-int(x[2]))
    if len(partidas)>5:
        partidas=partidas[:5]
    return partidas

# ------------------------------------------------------------------------
#| CODIGO  CODIGO  CODIGO  CODIGO  CODIGO  CODIGO  CODIGO  CODIGO  CODIGO |
# ------------------------------------------------------------------------ 

exit=False
partidas=False
while exit==False:
    clear()
    print("")
    print("¡Bienvenido al ahorcado!"+"""\n  _____\n |     O\n |    /|\\\n |    / \\\n_|_""")
    print("\nIngrese \"0\" para comenzar a jugar, \n        \"1\" para mostrar el ranking,\n        \"2\" para mostrar los creditos, o \n        \"3\" para salir.")
    ans=input("* ")

    if ans=="0":
        if partidas==True:
            clear()
            print("\n¡Saludos, jugador!\nUsted ya ingreso una lista de palabras previamente.\n¿Quiere utilizar la misma lista?\nIngrese \"0\" para crear una lista nueva, o\npresione enter para continuar.")
            if input("* ")=="0":
                partidas=False
        if partidas==False:
            clear()
            palabras=[]
            esc=False
            print("\n¡Saludos, jugador!\nEl juego elegira una palabra de las que escriba a continuacion, para que intenten adivinar.\nSi no ingresa ninguna, se utilizara una de las palabras por defecto.\nIngrese \"0\" cuando haya acabado.")
            while esc==False:
                palabra=input("* ")
                if palabra!="0" and palabra!="":
                    palabra=palabra.lower()
                    palabras.append(palabra)
                elif palabra=="0":
                    esc=True
                    paltype="Custom"
                    if palabras==[]:
                        palabras=lista.palabras
                        paltype="Default"
            partidas=True
        clear()

        palabra=palabras[random.randint(0,len(palabras)-1)]
        lineas="_ "*(len(palabra)-1)+"_"

        error=0
        LetrasUsadas=""
        win=False
        ahorcado(error)
        print(lineas)
        while error!=6 and win!=True:
            letra=""
            while letra in LetrasUsadas or len(letra)!=1:
                print("")
                letra=input("Escriba una letra: ")
                letra=letra.lower()
                clear()
                if letra in LetrasUsadas:
                    clear()
                    ahorcado(error)
                    print(lineas,"\n")
                    print("Letras usadas:",LetrasUsadas)
                    print("Ya utilizo esa letra")
                if len(letra)!=1 and letra!=palabra:
                    clear()
                    ahorcado(error)
                    print(lineas,"\n")
                    print("Letras usadas:",LetrasUsadas)
                    print("Debe escribir una letra")
                if letra==palabra:
                    lineas=" ".join(palabra)
                    error=-1
                    break
            
            if letra!=palabra:
                LetrasUsadas+=letra
            
            indices=[]
            for a in range(len(palabra)):
                if palabra[a]==letra:
                    indices.append(a)
            
            if indices==[]:
                error+=1
            ahorcado(error)

            if error!=6:
                lineas=lineas.split()
                for a in indices:
                    lineas[a]=letra
                lineas=" ".join(lineas)
                print(lineas,"\n")
                print("Letras usadas:",LetrasUsadas)

                if lineas.count("_")==0:
                    clear()
                    ganador()
                    win=True
            else:
                for f in range(3):
                    ahorcado(error)
                print("\n¡Perdiste!\nLa palabra era \""+str(palabra)+"\"")
                input()
        
        i=10
        while i>0:
            clear()
            print("¿Quiere guardar su puntaje?\nIngrese \"0\" para registrarlo, o\nenter para volver al menu.\n"+str(i)+"...")
            time.sleep(1)
            if kbhit():
                if kbget()=="0":
                    i=0
                    clear()
                    agregar([input("¡Jugador!\nIngrese aqui su nombre: "),len(LetrasUsadas),len(palabra),paltype])
                    ans="1"
                else:
                    i=0
            i-=1

    if ans=="1":
        clear()
        print("Top 5 de jugadores\n")
        try:
            top=top5()
        except:
            top=[]
        esp0=8
        esp1=9
        esp2=14
        for a in range(len(top)):
            if len(top[a][0])>esp0:
                esp0=len(top[a][0])+1
            if len(top[a][1])>esp1:
                esp1=len(top[a][1])+1
            if len(top[a][2])>esp2:
                esp2=len(top[a][2])+1
        print(getattr(colorama.Fore, "GREEN")+"Jugador"+" "*(esp0-7)+"|"+"Intentos"+" "*(esp1-8)+"|"+"Largo Palabra"+" "*(esp2-13)+"|"+"Tipo Palabra"+colorama.Style.RESET_ALL)
        for a in top:
            print(a[0]+(esp0-len(a[0]))*" "+"|"+a[1]+(esp1-len(a[1]))*" "+"|"+a[2]+(esp2-len(a[2]))*" "+"|"+a[3])
        input()

    if ans=="2":
        clear()
        print("""Integrantes del grupo:
  * Nicolas Cartalla
        nicolas.cartalla@correo.ucu.edu.uy
  * Valentina Cabrera
        valentina.cabreram@correo.ucu.edu.uy
Repositorio del Juego:
        https://github.com/nicocartalla/ahorcado.git""")
        input()

    if ans=="3":
        exit=True
        clear()