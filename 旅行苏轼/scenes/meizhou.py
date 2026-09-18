import pygame
import threading
import queue
import config
import data
from ai_handler import ask_ai
import json
from tools import Message, StoryBox, split_text
from poetry_ui import PoetryUI


class Item:
    def __init__(self, item_x, item_y, item_type, item_shape, item_color):
        self.x = item_x
        self.y = item_y
        self.type = item_type
        self.shape = item_shape
        self.color = item_color
        self.length, self.width, self.radius = 60, 40, 50
        self.created = False
        # 预先生成碰撞箱
        self.rect = pygame.Rect(self.x - 10, self.y - 10, self.radius, self.radius)

    def draw(self, screen):
        if self.shape == "ellipse":
            pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.length, self.width))
        elif self.shape == "circle":
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        elif self.shape == "rectangle":
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.length))    

    



def run_scene(screen):
    story_box = StoryBox(screen)
    stone_story = [{"speaker": "苏轼", "text": "这块砚台是我十二岁那年得来的。"},
    {"speaker": "少年苏辙", "text": "爹爹，子瞻得了一块奇石！"},
    {"speaker": "少年苏轼", "text": "这石头中间凹陷下去一块，真是奇妙。"},
    {"speaker": "石头", "text": "。。。"},
    {"speaker": "苏洵", "text": "不错，我看啊，这是天上的砚台。你在哪儿找到的？我们去刻字纪念一下。"},
    {"speaker": "少年苏轼", "text": "天上有仙人吗？真想去看一看啊。"},
    {"speaker": "少年苏辙", "text": "天上……应该比眉山更寒凉，阿兄要注意保暖啊。"} ]
    book_story = [{"speaker":"苏轼","text":"不知兄台是否有习举业？\n"},
                  {"speaker":data.player_name,"text":"未曾。"},
                  {"speaker":"苏轼","text":"无妨，这正是家父从益州府淘来的秋闱要集，不妨同观。"},
                  {"speaker":"少年苏轼","text":"坏了，坏了！"},
                  {"speaker":"少年苏辙","text":"出了什么事？"},
                  {"speaker":"少年苏轼","text":"卯君啊，我完全忘了背那秋闱集子里的范文！"},
                  {"speaker":"少年苏辙","text":"提醒的好，等你待会挨打时我可要躲远些。"}]
    font_name = pygame.font.Font(config.SIM_HEI, 18)
    # 初始旁白队列
    messages = []
    current_msg_idx = 0

    try:
        bg_image = pygame.image.load(config.IMG_MEIZHOU).convert()
        bg_image = pygame.transform.scale(bg_image, (800, 600))
    except Exception as e:
        print(f"加载眉州背景图失败：{e}")
        bg_image = pygame.Surface((800, 600))
        bg_image.fill(config.XUAN_PAPER)
    
    import os
    ss_json_path = os.path.join("prompts","ss_meizhou.json")
    with open(ss_json_path, 'r', encoding = 'utf-8') as f:
        ss_personal_data = json.load(f)
    
    if not hasattr(data, 'ss_history'):
        data.ss_history = []
    ai_response_queue = queue.Queue()

    items = [
        Item(300, 100, "stone", "ellipse", config.STONE), 
        Item(500, 170, "book", "rectangle", config.BOOK)
    ]
    rect_return_path = pygame.Rect(0, 570, 800, 30)
    
    # 初始旁白队列
    if data.introduction_played == False:
        messages = [
            Message("神秘声音", "你来到了眉山，此时，正是嘉祐元年..."),
            Message("神秘声音", "今年，苏轼二十一岁，但他实际上只有十九岁，还是一个年轻人。"),
            Message("神秘声音", "他要和弟弟子由和父亲苏洵一起，去汴京赶考了。")
        ]
        data.introduction_played=True
    else:
        messages = []
    current_msg_idx = 0

    input_active = False
    input_text = ""
    input_rect = pygame.Rect(100,550,600,32)
    
    #唱和ui
    poetry_ui = PoetryUI(screen, "眉州", ss_personal_data, data.ss_history)
    scroll_img = pygame.image.load(config.IMG_SCROLL).convert_alpha()
    scroll_img = pygame.transform.scale(scroll_img, (80,60))
    rect_scroll = pygame.Rect(650, 80, 80, 60)

    # 物品触发的台词
    echo = ""
    echo_time = 0
    showing_echo = False
    clock = pygame.time.Clock()
    running = True
    pygame.key.start_text_input()
    
    while running:
        # 【核心修复 1】每帧最开始，必须先画背景！用来覆盖上一帧的残影
        screen.blit(bg_image, (0, 0))
        story_box.update()
        poetry_ui.update()
        new_msgs = poetry_ui.get_pending_messages()
        if new_msgs:
            messages.extend(new_msgs)

        # 处理队列中的AI回复
        while not ai_response_queue.empty():
            reply = ai_response_queue.get()
            segments = split_text(reply, 15)
            for seg in segments:
                messages.append(Message("苏轼", seg))
            data.ss_history.append({"role":"assistant","content": reply})
            data.chat_count+=1
            data.introduction_played = True

        # 事件处理
        for event in pygame.event.get():
            if story_box.active:
                story_box.handle_event(event)
            if poetry_ui.active:
                poetry_ui.handle_event(event)
            else:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.TEXTINPUT:
                    if input_active:
                        input_text += event.text
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "LOBBY"  # 统一处理 ESC 键
                    if event.key == pygame.K_RETURN:
                        if not input_active:
                            input_active = True
                        else:
                            if input_text.strip():
                                player_msg = Message(data.player_name, input_text)
                                player_msg.start()
                                messages.append(player_msg)
                                data.ss_history.append({"role":"user","content":input_text})
                                # 调用AI（线程）
                                def fetch_ai():
                                    reply = ask_ai(ss_personal_data,data.ss_history,poetry_mode= False)
                                    ai_response_queue.put(reply)
                                threading.Thread(target=fetch_ai, daemon=True).start()
                                input_text = ""
                                input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        if input_active:
                            input_text = input_text[:-1]
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if rect_scroll.collidepoint(mouse_pos):
                        print("开启唱和")
                        poetry_ui.start()
                    elif rect_return_path.collidepoint(mouse_pos):
                        print("点击回程")
                        return "SMAP"
                
                # 【核心修复 2】必须在这里遍历所有物品，检查哪一个被点击了
                    for item in items:
                        if item.rect.collidepoint(mouse_pos):
                            showing_echo = True
                            echo_time = pygame.time.get_ticks()
                            # 根据点击的物品赋予不同的台词
                            if item.type == "stone":
                                echo = "一块漂亮的玉石，是从何得来的呢？"
                                story_box.start_story(stone_story, duration=3500)
                            elif item.type == "book":
                                echo = "一本被翻了许多次的书，中举之后，是不是就不需要再被父亲考校了？"
                                story_box.start_story(book_story,duration=3500)
        # 玩家名字标签（在背景图之后绘制，才不会被覆盖）
        name_tag = pygame.font.Font(config.SIM_SUN, 20).render(f"玩家：{data.player_name}", True, config.BLACK)
        screen.blit(name_tag, (10, 10))
        
        # 物品绘制
        for item in items:
            item.draw(screen)    
            # 【核心修复 3】删除了这里每帧自动刷新 echo 的错误逻辑

        # 物品交互文字显示
        if showing_echo:
            if pygame.time.get_ticks() - echo_time > 2000:
                showing_echo = False
            else:
                echo_pic = pygame.font.Font(config.SIM_HEI, 24).render(echo, True, config.BLACK)
                screen.blit(echo_pic, (200, 550))
        # 卷轴绘制
        if not poetry_ui.active:
            screen.blit(scroll_img, rect_scroll)
        poetry_ui.draw()
        
        # 旁白队列绘制
        if current_msg_idx < len(messages):
            msg = messages[current_msg_idx]
            if not msg.active and not msg.finished:
                msg.start()
            msg.draw(screen)
            if msg.finished:
                current_msg_idx += 1

        # 输入框绘制
        if input_active:
            pygame.draw.rect(screen, (240, 240, 240), input_rect)
            pygame.draw.rect(screen, config.BLACK, input_rect, 2)
            input_surf = pygame.font.Font(config.SIM_SUN, 40).render(input_text, True, config.BLACK)
            screen.blit(input_surf, (input_rect.x + 5, input_rect.y + 5))

        story_box.draw()

        pygame.display.flip()
        clock.tick(60)
        
    return "LOBBY"