import pygame
import config
import data
import random
import json
import letters_ui
from tools import Message, split_text

class Relics:
    def __init__(self, relic_x, relic_y, relic_type, relic_pic):
        self.x = relic_x
        self.y = relic_y
        self.type = relic_type
        self.pic = relic_pic
        self.created = False
        # 预先生成碰撞箱
        self.rect = pygame.Rect(self.x - 10, self.y - 10, self.radius, self.radius)


class MailSystem:
    def __init__(self, player_name, game_days, visited_locations, inventory):
        self.player_name = player_name
        self.game_days = game_days
        self.visited_locations = visited_locations
        self.inventory = inventory
        self.sent_letter_ids = []  # 已寄出的信ID
        self.pending_letter = None  # 待显示的信件（只有一封，一次只显示一封）
        
        # 加载所有信件
        import os
        letters_path = os.path.join("prompts", "letters.json")
        with open(letters_path, "r", encoding="utf-8") as f:
            self.all_letters = json.load(f)
    
    def update(self, current_game_days, visited_locations, inventory):
        """更新状态，并尝试生成新信（如果有待显示的信就不生成新的）"""
        self.game_days = current_game_days
        self.visited_locations = visited_locations
        self.inventory = inventory
        
        # 如果已经有待显示的信，不生成新的
        if self.pending_letter is not None:
            return
        
        self._check_new_letters()
    
    def _check_new_letters(self):
        """检查是否有新信可以寄出（30%概率）"""
        if random.random() > 0.7:  # 70%概率不产生新信
            return
        
        available = []
        for letter in self.all_letters:
            if letter["id"] in self.sent_letter_ids:
                continue
            if self.game_days >= letter.get("unlock_day", 0):
                available.append(letter)
        
        if not available:
            return
        
        # 按权重随机选一封
        weights = [l.get("weight", 5) for l in available]
        chosen = random.choices(available, weights=weights, k=1)[0]
        
        # 替换信中的玩家名字
        content = chosen["content"].replace("{player_name}", self.player_name)
        
        # 存储待显示的信件（不创建Message对象，只存原始数据）
        self.pending_letter = {
            "title": chosen["title"],
            "sender": chosen["sender"],
            "content": content,
            "gift":chosen.get("gift")
        }
        self.sent_letter_ids.append(chosen["id"])
        print(f"新信产生：{chosen['title']}")
    
    def has_pending_letter(self):
        """是否有待显示的信件"""
        return self.pending_letter is not None
    
    def get_pending_letter(self):
        """获取待显示的信件，并清空"""
        letter = self.pending_letter
        self.pending_letter = None
        return letter
    
def enter_player_name(screen):
    
    clock = pygame.time.Clock()
    input_box = pygame.Rect(250, 250, 300, 50)
    text = "莫任明"
    editing_text = ""
    pygame.key.start_text_input()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "EXIT"
            if event.type == pygame.TEXTINPUT:
                if len(text) < 12: text += event.text
            if event.type == pygame.TEXTEDITING:
                editing_text = event.text
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and text: return text
                if event.key == pygame.K_BACKSPACE: text = text[:-1]
        
        screen.fill(config.WHITE)
        prompt = pygame.font.Font(config.SIM_SUN, 40).render("请输入你的名字：", True, config.BLACK)
        screen.blit(prompt, (250, 180))
        pygame.draw.rect(screen, config.BLACK, input_box, 2)
        
        display_str = text + editing_text
        name_surf = pygame.font.Font(config.SIM_SUN, 40).render(display_str, True, config.BLACK)
        screen.blit(name_surf, name_surf.get_rect(center=input_box.center))
        pygame.display.flip()
        clock.tick(60)

def run_scene(screen):
    # 名字输入（保持不变）
    if data.player_name_is_named == False:
        data.player_name = enter_player_name(screen)
        data.player_name_is_named = True
        if not data.player_name:
            pygame.quit()
            exit()
    
    # 创建信件系统和信纸UI
    mail_system = MailSystem(
        player_name=data.player_name, 
        game_days=data.game_days, 
        visited_locations=data.visited_locations, 
        inventory=data.inventory
    )
    letter_paper = letters_ui.LetterPaper(screen)  # 新增信纸
    
    # 初始旁白
    if data.introducted is False:
        messages = [
            Message(data.player_name, "这是哪里？"),
            Message("神秘声音", "欢迎来到【旅行苏轼】，我们没有抄袭旅行青蛙。"),
            Message("神秘声音", "看到左边的门了吗？那里通往现实。"),
            Message("神秘声音", "右边的门，则通往苏轼的一生。")
        ]
        data.introducted = True
    else:
        messages = []
    
    current_msg_idx = 0
    
    # 加载背景
    try:
        bg_image = pygame.image.load(config.IMG_LOBBY).convert()
        bg_image = pygame.transform.scale(bg_image, (800, 600))
    except Exception as e:
        print(f"加载草庐背景图失败：{e}")
        bg_image = pygame.Surface((800, 600))
        bg_image.fill(config.XUAN_PAPER)
    
    # 点击区域
    rect_left_door = pygame.Rect(0, 195, 95, 290)
    rect_right_door = pygame.Rect(520, 127, 280, 356)
    rect_shelf = pygame.Rect(165, 329, 145, 184)
    rect_calligraphy = pygame.Rect(388, 160, 68, 252)
    rect_mail = pygame.Rect(270, 236, 59, 108)
    clock = pygame.time.Clock()
    running = True
    last_day_update = pygame.time.get_ticks()
    
    while running:
        screen.blit(bg_image, (0, 0))
        
        # 时间推进
        now = pygame.time.get_ticks()
        if now - last_day_update > 1800000:  # 半小时一天
            data.game_days += 1
            last_day_update = now
            mail_system.update(data.game_days, data.visited_locations, data.inventory)
        
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"
            
            # 鼠标点击
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                # 如果信纸在显示，优先关闭信纸
                if letter_paper.active:
                    letter_paper.handle_click(mouse_pos)
                    continue  # 跳过其他点击
                
                # 处理各种点击
                if rect_left_door.collidepoint(mouse_pos):
                    leaving = Message("神秘声音", "您要离开游戏吗？按ESC离开。")
                    messages.append(leaving)
                elif rect_right_door.collidepoint(mouse_pos):
                    return "SMAP"
                elif rect_mail.collidepoint(mouse_pos):
                    print("点击了竹筒，检查信件")
                    # 检查是否有新信
                    mail_system.update(data.game_days, data.visited_locations, data.inventory)
                    if mail_system.has_pending_letter():
                        letter = mail_system.get_pending_letter()
                        letter_paper.show(letter["title"], letter["sender"], letter["content"])
                        if letter.get("gift"):
                            gift = letter["gift"]
                            if not any(item.get("item_id")==gift["item_id"] for item in data.inventory):
                                data.inventory.append(gift)
                                gift_msg = Message("神秘声音", f"获得物品:【{gift['name']}】已存入博古架")
                                messages.append(gift_msg)
                            else:
                                pass
                    else:
                        no_mail = Message("系统", "柜子里空空如也，还没有新信。")
                        messages.append(no_mail)
                elif rect_shelf.collidepoint(mouse_pos):
                    print("点击了博古架")
                    if data.inventory:
                        names = "、".join([item["name"] for item in data.inventory])
                        msg_names = Message("神秘声音", f"博古架上陈列着：{names}")
                        messages.append(msg_names)
                        
                        # 再逐条展示每个物品的描述
                        for item in data.inventory:
                            msg_content = Message(f"【{item['name']}】", f"{item['description']}")
                            messages.append(msg_content)
                    else:
                        msg_empty = Message("神秘声音", "博古架上空空如也。")
                        messages.append(msg_empty)
                elif rect_calligraphy.collidepoint(mouse_pos):
                    print("点击了挂画")
            
            # 键盘事件
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "EXIT"
        
        # 绘制
        name_tag = pygame.font.Font(config.SIM_SUN, 20).render(f"玩家：{data.player_name}", True, config.BLACK)
        screen.blit(name_tag, (10, 10))
        
        # 如果没有显示信纸，才显示消息队列
        if not letter_paper.active:
            if current_msg_idx < len(messages):
                msg = messages[current_msg_idx]
                if not msg.active and not msg.finished:
                    msg.start()
                msg.draw(screen)
                if msg.finished:
                    current_msg_idx += 1
        
        # 绘制信纸（会在最上层）
        letter_paper.draw()
        
        pygame.display.flip()
        clock.tick(60)
    
    return "EXIT"