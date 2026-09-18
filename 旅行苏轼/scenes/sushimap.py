import pygame
import config
import data

class Message:

    def __init__(self, speakername, sentence):
        self.text = sentence
        self.speaker = speakername
        self.x, self.y = 10, 550
        self.show_time = 0
        self.active = False # 是否正在显示
        self.finished = False # 是否播完了

    def start(self):
        self.active = True
        self.show_time = pygame.time.get_ticks()

    def draw(self, screen):
        if not self.active: return
        elapsed = pygame.time.get_ticks()-self.show_time
        chars_to_show = elapsed//50
        current_time = pygame.time.get_ticks()
        if current_time - self.show_time > 3000: # 每条显示3秒
            self.active = False
            self.finished = True
            return
        current_display_text = self.text[:chars_to_show]
        message_text= f"{self.speaker}: {current_display_text}"

        message_pic = pygame.font.Font(config.SIM_HEI, 24).render(message_text, True, config.BLACK)
        screen.blit(message_pic, (self.x, self.y))


def run_scene(screen):
    # 初始旁白队列
    messages = [
    ]
    current_msg_idx = 0
    
    try:
        bg_image = pygame.image.load(config.IMG_MAP).convert()
        bg_image = pygame.transform.scale(bg_image, (800, 600))
    except Exception as e:
        print(f"加载湖边背景图失败：{e}")
        bg_image = pygame.Surface((800, 600))
        bg_image.fill(config.XUAN_PAPER)

    rect_meizhou = pygame.Rect(112, 216, 40, 40)
    rect_return_path = pygame.Rect(0, 570, 800, 30)

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(bg_image, (0,0))
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if rect_meizhou.collidepoint(mouse_pos):
                    print("点击眉州")
                    return "MEIZHOU"
                elif rect_return_path.collidepoint(mouse_pos):
                    print("点击回程")
                    return "CR"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "EXIT"

        # 绘制
        name_tag = pygame.font.Font(config.SIM_SUN, 20).render(f"玩家：{data.player_name}", True, config.BLACK)
        screen.blit(name_tag, (10, 10))
        

        pygame.display.flip()
        clock.tick(60)
    return "EXIT"