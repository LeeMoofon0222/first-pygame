import pygame as pg
import random
import os

#貞數
fps=60
#視窗大小
width=600 
height=600
#顏色
white=(255,255,255)
green=(0,255,0)
red=(255,0,0)
yellow=(255,255,0)
black=(0,0,0)


pg.init()#遊戲初始化
pg.mixer.init()#音樂初始化
screen=pg.display.set_mode((width,height))#視窗大小
pg.display.set_caption("Spacejunk")#遊戲標題
clock=pg.time.Clock()#建立一個物件，對時間做管理及操控

#載入特效
THE_POWER = {}
THE_POWER['shield'] = pg.image.load(os.path.join("C:\python圖片\shield.png")).convert()
THE_POWER['gun'] = pg.image.load(os.path.join("C:\python圖片\gun.png")).convert()

#載入圖片
THE_BACKGROUND=pg.image.load(os.path.join("C:\python圖片\背景.gif")).convert()
THE_PLAYER=pg.image.load(os.path.join("C:\python圖片\飛船.jpg")).convert()
THE_MPLAYER=pg.transform.scale(THE_PLAYER,(30,28))
THE_MPLAYER.set_colorkey(white)
THE_BULLETS=pg.image.load(os.path.join("C:\python圖片\子彈.jpg")).convert()
THE_JCP=pg.image.load(os.path.join("C:\python圖片\JCP.jpg")).convert()
THE_DIAMOND=pg.image.load(os.path.join("C:\python圖片\鑽石.png")).convert()
THE_ROCKS=[]#建立一個列表，用來放所有種類的石頭
for i in range(1,8):
    THE_ROCKS.append(pg.image.load(os.path.join(f"C:\python圖片\石頭{i}.png")).convert())

expl_anim = {}#創立一字典，來存放大爆炸及小爆炸

expl_anim['player']=[]#飛船爆炸list
for i in range(9):
    player_expl = pg.image.load(os.path.join(f"C:\python圖片\player_expl{i}.png")).convert()
    player_expl.set_colorkey(black)
    expl_anim['player'].append(player_expl)

expl_anim['lg'] = []#大爆炸圖片list
expl_anim['se'] = []#小爆炸圖片list
#載入圖片並去背
for i in range(9):
    expl_img = pg.image.load(os.path.join(f"C:\python圖片\expl{i}.png")).convert()
    expl_img.set_colorkey(black)
    #更改爆炸尺寸(大及小)
    expl_anim['lg'].append(pg.transform.scale(expl_img, (75, 75)))
    expl_anim['se'].append(pg.transform.scale(expl_img, (30, 30)))


#載入音效
JCP_SOUND=pg.mixer.Sound(os.path.join("C:\python音效\JCP爆炸.mp3"))
DIAMOND_SOUND=pg.mixer.Sound(os.path.join("C:\python音效\鑽石爆炸聲.mp3"))
SHOOT_SOUND=pg.mixer.Sound(os.path.join("C:\python音效\射擊.mp3"))
#載入所有石頭的音樂
ROCK_SOUND=[
pg.mixer.Sound(os.path.join("C:\python音效\岩石爆炸1.mp3")),
pg.mixer.Sound(os.path.join("C:\python音效\岩石爆炸2.mp3")),
pg.mixer.Sound(os.path.join("C:\python音效\岩石爆炸3.mp3"))]
pg.mixer.music.load(os.path.join("C:\python音效\背景音樂.mp3"))
EXPLOTION_SOUND=[pg.mixer.Sound(os.path.join("C:\python音效\expl0.wav")),
                 pg.mixer.Sound(os.path.join("C:\python音效\expl1.wav"))]
DIE_SOUND=(pg.mixer.Sound(os.path.join("C:/python音效/rumble.ogg")))
SHIELD_SOUND=(pg.mixer.Sound(os.path.join("C:/python音效/pow0.wav")))
GUN_SOUND=(pg.mixer.Sound(os.path.join("C:/python音效/pow1.wav")))

font_name=pg.font.match_font('arial')#引入字體

#分數
def draw_text(surf,text,size,x,y):#寫的平面，文字大小，座標(分數)
    font=pg.font.Font(font_name,size)#創建文字物件
    text_surface=font.render(text,True,white)#文字渲染成白色
    text_rect=text_surface.get_rect()#定位文字
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)#畫出文字，平面，位置

#血條
def draw_health(surf,hp,x,y):
  #以免發生生命值為負數的情況
  if hp<0:
     hp=0
  Hlenth=50#生命條長
  Hheigh=10#生命條寬
  fill=(hp/100)*Hlenth#要把生命條填滿幾分之幾
  outline_rect=pg.Rect(x,y,Hlenth,Hheigh)#畫一矩形當作生命條外框
  fill_rect=pg.Rect(x,y,fill,Hheigh)#填滿外框
  if hp<=100 and hp>75:
     pg.draw.rect(surf,green,fill_rect)#畫生命值<100，>75時是綠色
  if hp<=75 and hp>25:
     pg.draw.rect(surf,yellow,fill_rect)#畫生命值<75，>25時是黃色
  if hp<25:
     pg.draw.rect(surf,red,fill_rect)#畫生命值<25時變紅色

#命數
def draw_lives(surf, live, img, x, y):
      #看還有幾條命
      for i in range(live):
        img_rect = img.get_rect()#定位圖片
        img_rect.x = x + 32*i#間隔32再畫一個飛船
        img_rect.y = y
        surf.blit(img, img_rect)#畫出圖片，位置

#ui介面
def draw_init():
    screen.blit(THE_BACKGROUND,(0,0))#載入圖片
    draw_text(screen,'Clean The Space',64,width/2,height/4)
    draw_text(screen, ' ↕←→:Move Your Spaceship  [Key_Space]:Shoot', 22, width/2, height/2)
    draw_text(screen, 'Press Any Botton To Start!', 18, width/2, height*3/4)
    pg.display.update()
    waiting = True
    #當鍵盤被按下去時
    while waiting:
        clock.tick(fps)
        # 取得輸入
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYUP:
                waiting = False
                return False


class Player(pg.sprite.Sprite):
  def __init__(self):
      pg.sprite.Sprite.__init__(self)#內建Sprite初始函式
      self.image=pg.transform.scale(THE_PLAYER,(45,45))#顯示飛船圖片，並調整尺寸
      self.image.set_colorkey(white)#去除白色背景 
      self.rect=self.image.get_rect()#定位圖片(把圖片框起來)
      self.radius=25#碰撞區域圓形半徑為25
      #pg.draw.circle(self.image,red,self.rect.center,self.radius)#飛船碰撞範圍的圓形
      #飛船一開始生成的位置
      self.rect.centerx=width/2
      self.rect.bottom=height-10
      self.speedx=8#飛船速度
      self.health=100#玩家生命
      self.life=3#玩家命數
      self.hidden=False#判斷飛船一開始是否為隱藏狀態
      self.hidden_time=0#隱藏時間
      self.gun=1#一開始只有一把槍
      self.gun_time=0#吃到閃電的時間

  def update(self):
      #讓閃電只維持6秒
      if self.gun > 1 and pg.time.get_ticks() - self.gun_time > 6000:
            self.gun -= 1
            self.gun_time = pg.time.get_ticks()
       
      #重新生成飛船
      if self.hidden and pg.time.get_ticks() - self.hide_time > 1000:#如果在隱藏中，而且當飛船時間-隱藏時間>1時
         self.hidden = False#顯示回來
         self.rect.centerx = width / 2
         self.rect.bottom = height - 10

      key_pressed=pg.key.get_pressed()#判斷鍵盤上的按鍵有沒有被按到
      if key_pressed[pg.K_RIGHT]:#判斷右鍵有沒有被按
         self.rect.x+=self.speedx
      if key_pressed[pg.K_LEFT]:#判斷左鍵有沒有被按
         self.rect.x-=self.speedx
      if key_pressed[pg.K_UP]:#判斷上鍵有沒有被按
         self.rect.y-=self.speedx
      if key_pressed[pg.K_DOWN]:#判斷下鍵有沒有被按
         self.rect.y+=self.speedx

      if self.rect.right>width:#讓飛船右邊的座標最多等於螢幕左邊
         self.rect.right=width
      if self.rect.left<0:#讓飛船左邊的座標最多等於螢幕左邊
         self.rect.left=0
      if self.rect.top<0:#讓飛船上邊的座標最多等於螢幕上邊
         self.rect.top=0
      if self.rect.bottom>height:#讓飛船下邊的座標最多等於螢幕下邊
         self.rect.bottom=height

  def shoot(self):
      if not(self.hidden):#當飛船不是在隱藏中
         if self.gun == 1:#只有一把槍時
           bullet=Bullet(self.rect.centerx,self.rect.top)#射擊出發點在飛船左右中點以及飛船頂部
           all_sprites.add(bullet)#all_sprites增加子彈(畫面增加子彈)
           bullets.add(bullet)#每射一個子彈，就補一個子彈
           SHOOT_SOUND.play()#射擊音效
         elif self.gun==2:#當槍有兩把時，射左右子彈
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                SHOOT_SOUND.play()
         elif self.gun>=3:#當槍有三把時，射左中右子彈
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                SHOOT_SOUND.play()

  def hide(self):
      self.hidden = True#飛船隱藏
      self.hide_time = pg.time.get_ticks()#隱藏時間
      self.rect.center = (width/2, height+500)#定位到畫面之外

  def gunup(self):
      self.gun+=1#增加一把槍
      self.gun_time = pg.time.get_ticks()

class Rock(pg.sprite.Sprite):
  def __init__(self):
      pg.sprite.Sprite.__init__(self)#內建Sprite初始函式
      self.image_ori=random.choice(THE_ROCKS)#隨機顯示一張石頭圖片
      self.image_ori.set_colorkey(black)#去背(黑色)
      self.image=self.image_ori.copy()#複製一張石頭圖
      self.rect=self.image.get_rect()#定位圖片
      self.radius=self.rect.width*0.9 /2#設定碰撞區域半徑
      #pg.draw.circle(self.image,red,self.rect.center,self.radius)#畫碰撞半徑圓
      self.rect.x=random.randrange(0,width-self.rect.width)#石頭生成的x座標介於0~視窗寬度減去石頭寬度(因為石頭也有寬度，所以不能直接用視窗寬度)
      self.rect.y=random.randrange(-180,-100)#石頭生成的y座標介於-180~-100間
      #讓每顆石頭速度不一樣
      self.speedx=random.randrange(-4,3)
      self.speedy=random.randrange(2,8)
      self.total_degree=0#設立一變數，代表石頭總共轉的度數
      self.rot_degree=random.randrange(-3,3)#讓石頭每次旋轉3度，可能是順OR逆時針

  def rotate(self):
      self.total_degree+=self.rot_degree#石頭總共轉的度數
      self.total_degree=self.total_degree%360#讓石頭不會轉太快
      self.image=pg.transform.rotate(self.image_ori ,self.total_degree)#將self.image轉成旋轉的self.image_ori圖片動畫，(要定位不會旋轉的物件，否則會失真)   
      center=self.rect.center
      self.rect=self.image.get_rect()#重新定位圖片(轉動過的self.image)
      self.rect.center=center#設定為原先的中心點

  def update(self):
      self.rotate()#轉動石頭
      #讓座標加上速度
      self.rect.x+=self.speedx
      self.rect.y+=self.speedy
      #如果石頭上邊大於視窗底邊OR左邊大於視窗右邊OR右邊小於視窗左邊，則石頭重新生成
      if self.rect.top>height or self.rect.left>width or self.rect.right<0:
         self.rect.x=random.randrange(0,width-self.rect.width)
         self.rect.y=random.randrange(-180,-10)
         self.speedx=random.randrange(-4,3)
         self.speedy=random.randrange(2,10)

class Bullet(pg.sprite.Sprite):
  def __init__(self,x,y):#傳入子彈的座標
      pg.sprite.Sprite.__init__(self)#內建Sprite初始函式
      self.image=pg.transform.scale(THE_BULLETS,(30,30))#顯示圖片，調整大小
      self.image.set_colorkey(black)#去除黑色背景
      self.rect=self.image.get_rect()#定位圖片(把圖片框起來)
      self.rect.centerx=x#x座標與飛船相同
      self.rect.bottom=y#x座標與飛船相同
      self.speedy=-12#子彈速度
  
  def update(self):
      self.rect.y+=self.speedy#讓Y座標加上速度
      #出了視窗，就刪除子彈
      if self.rect.bottom<0:
         self.kill()

class JCP(pg.sprite.Sprite):
  #同石頭
  def __init__(self):
      pg.sprite.Sprite.__init__(self)
      self.image_ori=pg.transform.scale(THE_JCP,(45,45))
      self.image_ori.set_colorkey(black)
      self.image=self.image_ori.copy()
      self.rect=self.image.get_rect()
      self.radius=self.rect.width*0.8/2
      self.rect.x=random.randrange(0,width-self.rect.width)
      self.rect.y=random.randrange(-180,-100)
      self.speedx=random.randrange(-3,3)
      self.speedy=random.randrange(2,4)
      self.total_degree=0
      self.rot_degree=random.randrange(-3,3)

  def rotate(self):
      self.total_degree+=self.rot_degree
      self.total_degree=self.total_degree%360
      self.image=pg.transform.rotate(self.image_ori ,self.total_degree)    
      center=self.rect.center
      self.rect=self.image.get_rect()
      self.rect.center=center

  def update(self):
      self.rotate()
      self.rect.x+=self.speedx
      self.rect.y+=self.speedy
      if self.rect.top>height or self.rect.left>width or self.rect.right<0:
         self.rect.x=random.randrange(0,width-self.rect.width)
         self.rect.y=random.randrange(-180,-100)
         self.speedx=random.randrange(-3,3)
         self.speedy=random.randrange(2,4)

class DAIMOND(pg.sprite.Sprite):
   #同石頭
   def __init__(self):
      pg.sprite.Sprite.__init__(self)
      self.image=pg.transform.scale(THE_DIAMOND,(30,30))
      self.image.set_colorkey(black) 
      self.rect=self.image.get_rect()
      self.radius=self.rect.width*1.1/2
      self.rect.x=random.randrange(0,width-self.rect.width)
      self.rect.y=0
      self.speedx=0
      self.speedy=2

   def update(self):
       self.rect.x+=self.speedx
       self.rect.y+=self.speedy
       if self.rect.top>height or self.rect.left>width or self.rect.right<0:
          self.rect.x=random.randrange(0,width-self.rect.width)
          self.rect.y=random.randrange(-180,-100)
          self.speedx=0
          self.speedy=2

class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):#爆炸中心點，爆炸尺寸
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]#看是大爆炸還是小爆炸，並取第一張圖片
        self.rect = self.image.get_rect()#定位
        self.rect.center = center
        self.frame = 0#現在更新到第幾張圖片
        #為什麼不用update函式?因為那樣會快到看不出動畫
        self.last_update = pg.time.get_ticks()#最後一次更新圖片等於初始化到現在所經過的毫秒數
        self.frame_rate = 50#每50毫秒換成下一張

    def update(self):
        now = pg.time.get_ticks()#現在更新的時間
        #如果now減去最後一次更新的時間大於50毫秒，時間重置，圖片更新下一張
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            #現在更新的圖片是否到最後一張，如果是，則刪除
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            #如果不是，則移到下一張圖片
            else:
                self.image = expl_anim[self.size][self.frame]
                #重新定位
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center  
  
class Power(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])#隨機選一個寶物
        self.image = THE_POWER[self.type]
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height:#當輔助器超出視窗時，刪除它
           self.kill()  

pg.mixer.music.play(-1)#播放背景音樂

#更新難度
def Score():
    for i in range(3):
        rock=Rock()
        all_sprites.add(rock)#加一顆石頭至all_sprites群組
        rocks.add(rock)#加一顆石頭至石頭群組

#一判斷條件G    
G=0

#遊戲迴圈
show_init=True
running=True
while running: 
  if show_init:#是否顯示初始畫面
    close=draw_init()
    if close:
       break
    show_init=False#畫完之後就不顯示
    all_sprites=pg.sprite.Group()#創建一個all_sprites的群組來放物件
    rocks=pg.sprite.Group()#創建一個石頭的群組來放物件石頭
    bullets=pg.sprite.Group()#創建一個子彈的群組來放子彈
    powers=pg.sprite.Group()#創建一個輔助器的群組來放輔助器

    jcps=pg.sprite.Group()#創建一個jcps的群組來放jcp
    jcp=JCP()
    all_sprites.add(jcp)#加jcp至all_sprites群組
    jcps.add(jcp)#加jcp至JCP群組

    daimonds=pg.sprite.Group()#創建一個daimonds的群組來放diamonds
    daimond=DAIMOND()
    all_sprites.add(daimond)#加daimond至all_sprites群組
    daimonds.add(daimond)#加daimond至daimonds群組

    player=Player()
    all_sprites.add(player)#加player至all_sprites群組

    #開局生成5顆石頭
    for i in range(5):
        rock=Rock()
        all_sprites.add(rock)#加一顆石頭至all_sprites群組
        rocks.add(rock)#加一顆石頭至石頭群組

    score=0#設置分數


  clock.tick(fps)#設定成60貞，解決玩家電腦性能不一的問題

  #取得輸入，如果玩家點出去，則遊戲停止
  for event in pg.event.get():
    if event.type==pg.QUIT:
       running=False

    #如果玩家點擊空白鍵，則進入射擊函數
    elif event.type==pg.KEYDOWN:#偵測有無按鍵被按下
       if event.key==pg.K_SPACE:#偵測是否為空白鍵被按下D
          player.shoot()

  #更新遊戲
  all_sprites.update()#執行all_sprites裡每個物件的update函式 

  hits = pg.sprite.groupcollide(rocks, bullets, True, True)#偵測子彈是否與石頭碰撞，若碰撞則子彈與石頭都消失
  #爆炸動畫
  for hit in hits:
      random.choice(EXPLOTION_SOUND).play()
      score += hit.radius#加的分數等於石頭的半徑
      expl = Explosion(hit.rect.center,'lg')#大爆炸
      all_sprites.add(expl)
      if random.random() > 0.97:#掉寶機率3%
         pow = Power(hit.rect.center)
         all_sprites.add(pow)
         powers.add(pow)
      rock=Rock()
      all_sprites.add(rock)
      rocks.add(rock)

  #jcp碰撞，同石頭
  hits=pg.sprite.groupcollide(jcps,bullets,True,True)
  for hit in hits:
      JCP_SOUND.play()
      score-=250
      jcp=JCP()
      all_sprites.add(jcp)
      jcps.add(jcp)

  #鑽石碰撞，同石頭
  hits=pg.sprite.groupcollide(daimonds,bullets,True,True)
  for hit in hits:
      DIAMOND_SOUND.play()
      score+=100
      daimond=DAIMOND()
      all_sprites.add(daimond)
      daimonds.add(daimond)
  
  #如果是吃到鑽石(飛船碰到鑽石)，則額外加分，並加血量
  hits=pg.sprite.spritecollide(player,daimonds,True,pg.sprite.collide_circle)
  for hit in hits:
     DIAMOND_SOUND.play()
     daimond=DAIMOND()
     all_sprites.add(daimond)
     daimonds.add(daimond)
     player.health+=20
     score+=150
     if player.health > 100:
        player.health = 100

  #輔助器效果
  hits=pg.sprite.spritecollide(player,powers,True,pg.sprite.collide_circle)#偵測飛船是否有跟輔助器碰撞，並以圓形偵測
  for hit in hits:
      if hit.type == 'shield':
            player.health += 20
            if player.health > 100:
                player.health = 100
            SHIELD_SOUND.play()
      elif hit.type == 'gun':
            player.gunup()
            GUN_SOUND.play()
     

  hits=pg.sprite.spritecollide(player,jcps,True,pg.sprite.collide_circle)#偵測飛船是否有跟jcp碰撞，並以圓形偵測，True代表要不要刪除碰撞的物件
  #相撞後減少生命值並扣除分數
  for hit in hits:
     JCP_SOUND.play()
     jcp=JCP()
     all_sprites.add(jcp)
     jcps.add(jcp)
     player.health-=20
     score-=300


  hits=pg.sprite.spritecollide(player,rocks,True,pg.sprite.collide_circle)#偵測飛船是否有跟石頭碰撞，並以圓形偵測，True代表要不要刪除碰撞的物件
  #相撞後減少生命值
  for hit in hits:
     random.choice(ROCK_SOUND).play()
     rock=Rock()
     all_sprites.add(rock)
     rocks.add(rock)
     player.health-=hit.radius#減去石頭半徑的生命
     expl = Explosion(hit.rect.center,'se')#小爆炸
     all_sprites.add(expl)
     #死掉時
     if player.health<=0:
         die = Explosion(player.rect.center, 'player')
         all_sprites.add(die)
         DIE_SOUND.play()
         player.life-=1#命數減1
         player.health=100#生命回滿
         player.hide()#死掉之後有緩衝(隱藏飛船)
     #當沒命時回到初始畫面，並讓動畫跑完
  if player.life==0 and not (die.alive()):
        show_init=True

  #難度隨著分數增加(岩石變多)，G拿來當作判斷條件，以免函數不斷地跑
  if score>500 and G<1:
     Score()
     G+=1
  if score>1000 and G<2:
     Score()
     G+=1
  if score>2000 and G<3:
     Score()
     G+=1  
  if score>4000 and G<4:
     Score()
     G+=1
  if score>8000 and G<5:
     Score()
     G+=1
  if score>10000 and G<6:
     Score()
     G+=1
  if score>15000 and G<7:
     Score()
     G+=1
  if score>30000 and G<8:
     Score()
     G+=1
  if score>50000 and G<9:
     Score()
     G+=1
  if score>100000 and G<10:
     Score()
     G+=1
     
  #畫面顯示
  screen.fill(black)
  screen.blit(THE_BACKGROUND,(0,0))#載入圖片
  draw_health(screen,player.health,player.rect.centerx-25,player.rect.bottom)#畫出生命條
  draw_lives(screen,player.life,THE_MPLAYER,width-100,570)#畫出命數
  all_sprites.draw(screen)#畫出所有all_sprites的物件到螢幕上
  draw_text(screen,str(int(score)),18,width/2,15)#輸入分數函式值
  pg.display.update()

pg.quit

