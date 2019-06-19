# インストールした discord.py を読み込む
import discord
#rondomをインポート
import random
#osをインポート
import os


# 自分のBotのアクセストークン
TOKEN = os.environ['DISCORD_BOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    #様々な初期化
    global channels_states
    channels_states = {}       #ChID用の辞書
    global channel_nova
    channel_nova = {}

#52枚の山札
deck_52 = ["DIA　A","CLUB　A","HEART　A","SPADE　A","DIA　2","CLUB　2","HEART　2","SPADE　2",
    "DIA　3","CLUB　3","HEART　3","SPADE　3","DIA　4","CLUB　4","HEART　4","SPADE　4",
    "DIA　5","CLUB　5","HEART　5","SPADE　5","DIA　6","CLUB　6","HEART　6","SPADE　6",
    "DIA　7","CLUB　7","HEART　7","SPADE　7","DIA　8","CLUB　8","HEART　8","SPADE　8",
    "DIA　9","CLUB　9","HEART　9","SPADE　9","DIA　10","CLUB　10","HEART　10","SPADE　10",
    "DIA　J","CLUB　J","HEART　J","SPADE　J","DIA　Q","CLUB　Q","HEART　Q","SPADE　Q",
    "DIA　K","CLUB　K","HEART　K","SPADE　K"]

#54枚の山札
deck_54 = deck_52 + ["JOKER","JOKER"]

#108枚の山札
deck_108 = deck_54 *2

#ニューロデッキ
nova_deck = ["カブキ","バサラ","タタラ","ミストレス","カブト","カリスマ","マネキン","カゼ","フェイト","クロマク","エグゼク","カタナ","クグツ","カゲ","チャクラ","レッガー","カブトワリ","ハイランダー","マヤカシ","トーキー","イヌ","ニューロ","ヒルコ","クロガネ","アラシ","カゲムシャ","アヤカシ","イブキ","コモン","シキガミ","エトランゼ"]

#正位置と逆位置
position = ["正位置","逆位置"]

# メッセージ受信時に動作する処理
@client.event
async def on_message(message): 

    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

        #山札のセット　52枚編
        #「/52deck」と発言したらdeckの準備と「52枚の山札を用意しました」が返る処理と初期化
    if message.content == "/52deck":
        ch_id = message.channel.id  #メッセージが送信されたchのIDを定義
        channels_states.setdefault(ch_id, {})        #送信されたIDが辞書にない場合空辞書をつくる
        deck = copy.copy(deck_52)      #deckにdeck_52のリストと定義する
        trash_deck = []     #trash_deckのリストを空にする処理
        channels_states[ch_id]['deck'] = deck        #channels_statesのchidキー内のdeckキーにdeckを入れる処理
        channels_states[ch_id]['trash_deck'] = trash_deck
        await message.channel.send("52枚の山札を用意しました")  #メッセージの送信

    #山札のセット　54枚編
    #「/54deck」と発言したらdeckの準備と「54枚の山札を用意しました」が返る処理と初期化
    if message.content == "/54deck":
        ch_id = message.channel.id  #メッセージが送信されたchのIDを定義
        channels_states.setdefault(ch_id, {})
        deck = copy.copy(deck_54)
        trash_deck = []
        channels_states[ch_id]['deck'] = deck
        channels_states[ch_id]['trash_deck'] = trash_deck
        await message.channel.send("54枚の山札を用意しました")

    #山札のセット　108枚編
    #「/108deck」と発言したdeckの準備と「2セットの山札を用意しました」が返る処理と初期化
    if message.content == "/108deck":
        ch_id = message.channel.id  #メッセージが送信されたchのIDを定義
        deck = copy.copy(deck_108)
        channels_states.setdefault(ch_id, {})
        trash_deck = []     #trash_deckのリストを空にする処理
        channels_states[ch_id]['deck'] = deck
        channels_states[ch_id]['trash_deck'] = trash_deck
        await message.channel.send("2セットの山札を用意しました")


     #「/hand」で辞書を作る
    if message.content == '/hand':
        ch_id = message.channel.id  #メッセージが送信されたchのIDを定義
        user_id = message.author.id
        channels_states[ch_id].setdefault(user_id, [])  #チャンネルごとにユーザーIDを入れる処理
        msg = message.author.mention + "　手札リストを用意しました"
        await message.channel.send(msg)
        

    # 「/draw」と発言したら発言者に「引いたカード」が返る処理と手札に追加する処理
    if message.content == '/draw':
        ch_id = message.channel.id
        user_id = message.author.id
        deck = channels_states[ch_id]['deck']
        draw_card = random.choice(deck)         #deck（リスト）内からランダムに選んだものをdraw_cardと定義する
        hand_list = channels_states[ch_id][user_id]
        hand_list = hand_list.append(draw_card)  #ユーザー辞書の値にカードを追加する処理
        drawmsg = message.author.mention + draw_card        #メンションとdraw_cardをdrawmsgと定義する
        await message.channel.send(drawmsg)             #drawmsgをチャンネルに送る
        deck.remove(draw_card)   #deckから引いたカードを除く処理
    

    #「/mdraw」と発言したら「引いたカード」にマスクをして返る処理
    if message.content == '/mdraw':
        ch_id = message.channel.id
        user_id = message.author.id
        deck = channels_states[ch_id]['deck']
        draw_card = random.choice(deck)         #deck（リスト）内からランダムに選んだものをdraw_cardと定義する
        hand_list = channels_states[ch_id][user_id]
        hand_list = hand_list.append(draw_card)  #ユーザー辞書の値にカードを追加する処理
        mdrawmsg = message.author.mention + "||" + draw_card + "||"     #メンションとマスクしたdraw_cardをmdrawmsgと定義する
        await message.channel.send(mdrawmsg)    #drawmsgをチャンネルに送る
        deck.remove(draw_card)    #deckから引いたカードを除く処理


    #「/myhand」と発言したら持っているカードを返す処理
    if message.content == '/myhand':
        ch_id = message.channel.id
        user_id = message.author.id
        hand = channels_states[ch_id][user_id]
        msg = message.author.mention + "あなたの持っているカードは　" + str(hand) + "　です"
        handmsg = msg.replace('\\u3000',"　")
        await message.channel.send(handmsg)
    
    #「/mmyhand」と発言したら持っているカードにマスクをしてを返す処理
    if message.content == '/mmyhand':
        ch_id = message.channel.id
        user_id = message.author.id
        hand = channels_states[ch_id][user_id]
        msg = message.author.mention + "あなたの持っているカードは　" + "||" + str(hand) + "||" +"　です"
        handmsg = msg.replace('\\u3000',"　")
        await message.channel.send(handmsg)
    
    #「/deck」で山札の枚数を表示
    if message.content == '/deck':
        ch_id = message.channel.id
        deck = channels_states[ch_id]['deck']
        await message.channel.send("山札" + "　" + str(len(deck)) + "枚")

    #「/trash 」で手札を捨てる
    if message.content.startswith('/trash '):
        ch_id = message.channel.id
        user_id = message.author.id
        trash_num = message.content.split()[1]  #スペース後の数字をトラッシュナンバーと定義する
        num = int(trash_num)-1  #入れた文字を数値にしてー1する処理
        hand_list = channels_states[ch_id][user_id] #ユーザー辞書の要素をハンドリストとする定義する
        trash_card = hand_list[num]     #指定した番号のハンドリストをトラッシュカードと定義する　メッセージを送る時に使う
        hand_list.pop(num)   #ハンドリストからとラッシュカードを消す処理
        channels_states[ch_id]['trash_deck'].append(trash_card)      #トラッシュデッキにトラッシュカードを入れる処理
        await message.channel.send("　" + trash_card + "を捨てました")

    #「/return」で捨て札を手札に戻す
    if message.content == '/return':
        ch_id = message.channel.id
        user_id = message.author.id
        trash_deck = channels_states[ch_id]['trash_deck']
        return_card = trash_deck[-1]
        trash_deck.remove(return_card)
        channels_states[ch_id][user_id].append(return_card)
        await message.channel.send(message.author.mention + "　" + return_card + "を手札に戻しました")

    
    #「/tdraw」で捨て札からカードを引く
    if message.content == '/tdraw':
        ch_id = message.channel.id
        user_id = message.author.id
        deck = channels_states[ch_id]['trash_deck']
        draw_card = random.choice(deck)         #deck（リスト）内からランダムに選んだものをdraw_cardと定義する
        channels_states[ch_id][user_id].append(draw_card)  #ユーザー辞書の値にカードを追加する処理
        drawmsg = message.author.mention + draw_card        #メンションとdraw_cardをdrawmsgと定義する
        await message.channel.send(drawmsg)             #drawmsgをチャンネルに送る
        deck.remove(draw_card)

    #「/mtdraw」で捨て札からカードを引く
    if message.content == '/mtdraw':
        ch_id = message.channel.id
        user_id = message.author.id
        deck = channels_states[ch_id]['trash_deck']
        draw_card = random.choice(deck) #deck（リスト）内からランダムに選んだものをdraw_cardと定義する
        channels_states[ch_id][user_id].append(draw_card) #ユーザー辞書の値にカードを追加する処理
        drawmsg = message.author.mention + "||" + draw_card + "||"        #メンションとdraw_cardをdrawmsgと定義する
        await message.channel.send(drawmsg)             #drawmsgをチャンネルに送る
        deck.remove(draw_card)
        
    #「/dtrash n」で山札に手札を戻す（捨てる）
    if message.content.startswith('/dtrash '):
        ch_id = message.channel.id
        user_id = message.author.id
        trash_num = message.content.split()[1]  #スペース後の数字をトラッシュナンバーと定義する
        num = int(trash_num)-1  #入れた文字を数値にしてー1する処理
        hand_list = channels_states[ch_id][user_id] #ユーザー辞書の要素をハンドリストとする定義する
        trash_card = hand_list[num]     #指定した番号のハンドリストをトラッシュカードと定義する　メッセージを送る時に使う
        hand_list.pop(num)   #ハンドリストからとラッシュカードを消す処理
        channels_states[ch_id]['deck'].append(trash_card)        #トラッシュデッキにトラッシュカードを入れる処理
        await message.channel.send("　" + trash_card + "を山札に戻しました")

    #「/dreturn」で山札の一番後ろを手札に戻す
    if message.content == '/dreturn':
        ch_id = message.channel.id
        user_id = message.author.id
        deck = channels_states[ch_id]['deck']
        trash_deck = channels_states[ch_id]['trash_deck']
        return_card = deck[-1]
        deck.remove(return_card)
        channels_states[ch_id][user_id].append(return_card)
        await message.channel.send(message.author.mention + "　" + return_card + "を手札に戻しました")

    #「/trashdeck」で捨て札の枚数を表示
    if message.content.startswith('/trashdeck'):
        ch_id = message.channel.id
        deck = channels_states[ch_id]['trash_deck']
        await message.channel.send("捨て札　" + str(len(deck)) + "枚")

    #「/nova」と発言したらニューロデッキを用意する処理
    if message.content.startswith("/nova"):
        ch_id = message.channel.id
        channel_nova.setdefault(ch_id,{})
        neuro_deck = copy.copy(nova_deck)
        channel_nova[ch_id]['neuro'] = neuro_deck
        await message.channel.send("ニューロデッキを用意しました")

    # 「/neuro」と発言したら「引いたスタイル」が返る処理
    if message.content.startswith('/neuro'):
        ch_id = message.channel.id
        neuro_deck = channel_nova[ch_id]['neuro']
        neuro_card = random.choice(neuro_deck)      #引いたカードをneuro_cardと定義する
        tarot_position = random.choice(position)    #正位置か逆位置かをランダムにtarot_positionに定義する
        await message.channel.send(neuro_card + "　" + tarot_position )
        neuro_deck.remove(neuro_card)        #neuro_deckからneuro_cardを除く処理

    #「/key (スタイル名)」で入力された任意のスタイルをニューロデッキから除く
    if message.content.startswith('/key '):
        style = message.content.split()[1]      #/keyスペースのあとに入力された文字をstyleと定義する
        ch_id = message.channel.id
        neuro_deck = channel_nova[ch_id]['neuro']
        neuro_deck.remove(style)        #styleをニューロデッキから除く処理
        await message.channel.send("ニューロデッキから" + style + "を取り出しました")



    

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
