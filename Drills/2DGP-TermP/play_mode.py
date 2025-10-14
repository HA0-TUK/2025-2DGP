from pico2d import *
import game_framework
from player import Player
from building import RhythmManager

class PlayMode:
    def __init__(self):
        self.player = None
        self.rhythm_manager = None
        self.game_over = False
        self.victory = False
        self.last_judgment = None
        self.judgment_time = 0
        
    def enter(self):
        self.player = Player()
        self.rhythm_manager = RhythmManager()
        self.game_over = False
        self.victory = False
        
    def exit(self):
        pass
        
    def pause(self):
        pass
        
    def resume(self):
        pass
    
    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                # 스페이스바로 패링 시도
                if self.player.parry():
                    # 리듬 판정
                    judgment, success = self.rhythm_manager.try_hit()
                    self.last_judgment = judgment
                    self.judgment_time = 0
                    
                    # 실패 시 피해
                    if not success:
                        self.player.take_damage()
                        
            elif event.key == SDLK_r and (self.game_over or self.victory):
                # 게임 재시작
                self.__init__()
                self.enter()
                
            elif event.key == SDLK_ESCAPE:
                game_framework.quit()
    
    def update(self):
        if self.game_over or self.victory:
            return
            
        dt = game_framework.game_state.dt
        
        # 플레이어 업데이트
        self.player.update(dt)
        
        # 리듬 시스템 업데이트
        self.rhythm_manager.update(dt)
        
        # 판정 텍스트 시간 업데이트
        if self.last_judgment:
            self.judgment_time += dt
            if self.judgment_time > 1.0:  # 1초 후 사라짐
                self.last_judgment = None
        
        # 게임 오버 체크
        if not self.player.is_alive():
            self.game_over = True
        
        # 승리 체크
        if self.rhythm_manager.is_finished() and self.player.is_alive():
            self.victory = True
        
        # 자동 피해 (놓친 노트들)
        for note in self.rhythm_manager.active_notes:
            if note.judgment == 'miss' and not note.is_hit:
                self.player.take_damage()
                note.is_hit = True
    
    def draw(self):
        clear_canvas()
        
        # 배경 (Nine Sols 스타일의 어두운 배경)
        # pico2d는 배경색 설정이 제한적이므로 사각형으로 근사
        
        # 게임 요소들 그리기
        if not (self.game_over or self.victory):
            self.rhythm_manager.draw()
            self.player.draw()
            
            # 판정 결과 표시
            if self.last_judgment:
                self.draw_judgment()
        
        # UI 그리기
        self.draw_ui()
        
        # 게임 오버/승리 화면
        if self.game_over:
            self.draw_game_over()
        elif self.victory:
            self.draw_victory()
    
    def draw_judgment(self):
        """판정 결과 그리기"""
        # 판정에 따른 색상
        colors = {
            'perfect': (255, 255, 100),
            'good': (100, 255, 100),
            'bad': (255, 150, 100),
            'miss': (255, 100, 100)
        }
        
        # 간단한 사각형으로 판정 표시
        color = colors.get(self.last_judgment, (255, 255, 255))
        size = 40 if self.last_judgment == 'perfect' else 30
        
        x, y = 400, 450
        draw_rectangle(x - size, y - size//2, x + size, y + size//2)
    
    def draw_ui(self):
        """UI 그리기"""
        # 점수 표시 (간단한 바 형태로)
        score_width = min(self.rhythm_manager.score // 10, 200)
        draw_rectangle(580, 550, 580 + score_width, 570)
        
        # 콤보 표시
        if self.rhythm_manager.combo > 0:
            combo_size = min(self.rhythm_manager.combo * 3, 60)
            draw_rectangle(50 - combo_size//2, 550 - combo_size//2,
                          50 + combo_size//2, 550 + combo_size//2)
    
    def draw_game_over(self):
        """게임 오버 화면"""
        # 반투명 오버레이
        draw_rectangle(0, 0, 800, 600)
        
        # 게임 오버 텍스트 (사각형으로 근사)
        draw_rectangle(300, 280, 500, 320)
        
        # 재시작 안내
        draw_rectangle(250, 200, 550, 220)
    
    def draw_victory(self):
        """승리 화면"""
        # 반투명 오버레이
        draw_rectangle(0, 0, 800, 600)
        
        # 승리 텍스트
        draw_rectangle(300, 320, 500, 360)
        
        # 최종 점수
        final_score_width = min(self.rhythm_manager.score // 20, 300)
        draw_rectangle(250, 280, 250 + final_score_width, 300)
        
        # 최대 콤보
        max_combo_width = min(self.rhythm_manager.max_combo * 5, 300)
        draw_rectangle(250, 250, 250 + max_combo_width, 270)
        
        # 재시작 안내
        draw_rectangle(250, 180, 550, 200)
