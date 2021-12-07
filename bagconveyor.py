#importando bibliotecas
import cv2
import numpy as np
from time import sleep

#DEFININDO VALORES MÁXIMOS E MÍNIMOS PARA IDENTIFIFCAÇÃOD DE CONTORNOS
largura_min=60 #Largura minima do retangulo
altura_min=50 #Altura minima do retangulo
largura_max=200 #Largura max do retangulo
altura_max=150 #altura max do retangulo
p_linha=200 #posição maxima do lado esquerdo para identificação de contornos
offset=1 #Erro permitido entre pixel  

pos_linha=200 #Posição da linha de contagem 

delay= 100 #FPS do vídeo

#ZERANDO VARIAVEIS
detec = []
bags= 0

#FUNÇÃO PARA PEGAR CENTROS	
def pega_centro(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

#LEITURA DO VIDEO
cap = cv2.VideoCapture('Bag Loading Conveyor.mp4')


#LOOP
while True:
    #LEITURA DO FRAME DO VIDEO
    _, frame = cap.read()
    #CONVERTER COR PARA HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
     
    #DEFININDO RANGE DE CORES A SEREM FILTRADAS
    #NESTE CASO AJUSTEI PARA TONS PRÓXIMOS DO BRANCO
    lower_white = np.array([4,10,180])
    upper_white = np.array([20,30,255])
    #CRIAÇÃO DE MÁSCARA PARA LER O RANGE ESPECIFICADO
    mask = cv2.inRange(hsv, lower_white, upper_white)
    #TESTE PARA APICAÇÃO DE GAUSSIAN BLUR E DILATAÇÃO
    #TESTES NÃO FUNCIONARAM COMO DESEJADO
    #blur = cv2.GaussianBlur(mask,(5,5),0)
    #dilat = cv2.dilate(mask,np.ones((5,5)))
    
    #DEFININDO KERNEL PARA APLICAÇÃO DE MORPHOLOGICAL TRANSFORMATION
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    #APLICANDO TRANSFORMAÇÃO DE "CLOSE"
    dilatada = cv2.morphologyEx (mask, cv2. MORPH_CLOSE , kernel, iterations =8)
    #ACHANDO CONTORNOS
    contours, _= cv2.findContours(dilatada, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
    
   
    
    
    #PLOTANDO LINHA DE CONTAGEM
    cv2.line(frame, (25, pos_linha), (1200, pos_linha), (255,127,0), 3) 
    
    #LOOP PARA VALIDAÇÃO E DESENHO DE CONTORNOS
    for(i,c) in enumerate(contours):
        (x,y,w,h) = cv2.boundingRect(c)
        validar_contorno = (w >= largura_min and w<=largura_max) and (h >= altura_min and h<=altura_max) and x>p_linha
        if not validar_contorno:
            continue
        #PEGANDO CENTROIDES E PLOTANDO
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)        
        centro = pega_centro(x, y, w, h)
        detec.append(centro)
        cv2.circle(frame, centro, 4, (0, 0,255), -1)
        #CONTANDO SACOS QUE PASSAM PARA A LINHA
        for (x,y) in detec:
            if y<(pos_linha+offset) and y>(pos_linha-offset):
                bags+=1
                cv2.line(frame, (25, pos_linha), (1200, pos_linha), (0,127,255), 3)  
                detec.remove((x,y))
                print("BAGS : "+str(bags))        
    #ESCREVENDO VALOR DE CONTAGEM
    cv2.putText(frame, "BAGS : "+str(bags), (100, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),2)
    
    #REPRODUZINDO VIDEO
    cv2.imshow("Video" , frame)
    #REPRODUÇÃO DAS MASCARAS
    #cv2.imshow("close", dilatada)
    #cv2.imshow("mask", mask)
    
    #QUEBRANDO LOOPS CASO ESC PRESSIONADA
    if cv2.waitKey(50) == 27:
        break
    
cv2.destroyAllWindows()
cap.release()
