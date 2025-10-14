from pico2d import *
import math

class Player:
    def __init__(self):
        self.x = 400  # 화면 중앙
        self.y = 300
        self.width = 64
        self.height = 64
        
        # 패링 상태
        self.is_parrying = False
        self.parry_time = 0
        self.parry_duration = 0.3  # 패링 애니메이션 시간
        
        # 피격 상태
        self.is_hit = False
        self.hit_time = 0
        self.hit_duration = 0.5
        
        # 체력
        self.hp = 3
        self.max_hp = 3
        
        # 애니메이션 프레임
        self.frame = 0
        self.action = 'idle'  # idle, parry, hit
        
        # 색상 (Nine Sols 스타일)
        self.base_color = (100, 150, 255)  # 파란색 계열
        self.parry_color = (255, 200, 100)  # 황금색
        self.hit_color = (255, 100, 100)    # 빨간색
    
    def update(self, dt):
        # 패링 상태 업데이트
        if self.is_parrying:
            self.parry_time += dt
            if self.parry_time >= self.parry_duration:
                self.is_parrying = False
                self.parry_time = 0
                self.action = 'idle'
        
        # 피격 상태 업데이트
        if self.is_hit:
            self.hit_time += dt
            if self.hit_time >= self.hit_duration:
                self.is_hit = False
                self.hit_time = 0
                self.action = 'idle'
        
        # 프레임 업데이트
        self.frame = (self.frame + dt * 10) % 4
    
    def parry(self):
        """패링 액션 실행"""
        if not self.is_hit:  # 피격 중이 아닐 때만 패링 가능
            self.is_parrying = True
            self.parry_time = 0
            self.action = 'parry'
            return True
        return False
    
    def take_damage(self):
        """피해를 받음"""
        if not self.is_parrying:  # 패링 중이 아닐 때만 피해
            self.hp -= 1
            self.is_hit = True
            self.hit_time = 0
            self.action = 'hit'
            return True
        return False
    
    def draw(self):
        # 현재 상태에 따른 색상 결정
        if self.is_parrying:
            color = self.parry_color
            size_modifier = 1.2  # 패링 시 약간 커짐
        elif self.is_hit:
            color = self.hit_color
            size_modifier = 0.8  # 피격 시 약간 작아짐
        else:
            color = self.base_color
            size_modifier = 1.0
        
        # 플레이어 그리기 (간단한 원형으로)
        radius = int((self.width / 2) * size_modifier)
        
        # Nine Sols 스타일의 이펙트 (패링 시 빛나는 효과)
        if self.is_parrying:
            # 외곽 글로우 효과
            for i in range(3):
                alpha = 0.3 - (i * 0.1)
                glow_radius = radius + (i * 10)
                # pico2d에서는 원을 직접 그리는 함수가 없으므로 사각형으로 근사
                draw_rectangle(self.x - glow_radius, self.y - glow_radius, 
                             self.x + glow_radius, self.y + glow_radius)
        
        # 메인 캐릭터 그리기
        draw_rectangle(self.x - radius, self.y - radius, 
                      self.x + radius, self.y + radius)
        
        # HP 표시
        self.draw_hp_bar()
    
    def draw_hp_bar(self):
        """체력바 그리기"""
        bar_width = 100
        bar_height = 10
        bar_x = self.x - bar_width // 2
        bar_y = self.y + 50
        
        # 배경
        draw_rectangle(bar_x - 2, bar_y - 2, bar_x + bar_width + 2, bar_y + bar_height + 2)
        
        # 체력바
        hp_width = int((self.hp / self.max_hp) * bar_width)
        if hp_width > 0:
            draw_rectangle(bar_x, bar_y, bar_x + hp_width, bar_y + bar_height)
    
    def is_alive(self):
        return self.hp > 0
    
    def get_parry_window(self):
        """패링 판정 윈도우 반환 (패링 중인지 확인)"""
        return self.is_parrying
