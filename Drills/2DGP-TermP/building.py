from pico2d import *
import time
import math
import random

class RhythmNote:
    """리듬 노트 클래스"""
    def __init__(self, beat_time, note_type='normal'):
        self.beat_time = beat_time  # 언제 쳐야 하는지
        self.note_type = note_type  # 노트 타입
        self.is_hit = False
        self.judgment = None  # 'perfect', 'good', 'bad', 'miss'
        
        # 시각적 표현
        self.x = 800  # 화면 오른쪽에서 시작
        self.y = 300
        self.target_x = 400  # 플레이어 위치
        self.size = 30
        
    def update(self, dt, current_time):
        """노트 업데이트"""
        # 노트가 목표 지점으로 이동
        time_to_beat = self.beat_time - current_time
        if time_to_beat > 0:
            # 2초 전부터 노트가 나타남
            progress = max(0, (2.0 - time_to_beat) / 2.0)
            self.x = 800 - (400 * progress)
        else:
            self.x = self.target_x
    
    def draw(self, current_time):
        """노트 그리기"""
        if self.is_hit:
            return
            
        # 노트가 화면에 나타날 시간인지 확인
        time_to_beat = self.beat_time - current_time
        if time_to_beat > 2.0:  # 2초 전부터 표시
            return
            
        # 노트 색상 (박자에 가까워질수록 밝게)
        if time_to_beat < 0.1:
            color = (255, 255, 100)  # 노란색 (타이밍!)
        elif time_to_beat < 0.3:
            color = (255, 200, 100)  # 주황색
        else:
            color = (100, 200, 255)  # 파란색
        
        # 노트 그리기
        half_size = self.size // 2
        draw_rectangle(self.x - half_size, self.y - half_size,
                      self.x + half_size, self.y + half_size)
        
        # 타이밍 가이드 라인 (세로선으로 근사)
        if abs(time_to_beat) < 0.5:
            line_width = 2
            draw_rectangle(self.target_x - line_width//2, self.y - 40,
                          self.target_x + line_width//2, self.y + 40)

class RhythmManager:
    """리듬 게임 관리자"""
    def __init__(self):
        self.bpm = 120  # 분당 박자 수
        self.beat_interval = 60.0 / self.bpm  # 박자 간격
        self.start_time = time.time()
        self.current_time = 0
        
        # 노트 리스트
        self.notes = []
        self.active_notes = []
        
        # 판정 관련
        self.perfect_window = 0.05  # ±0.05초
        self.good_window = 0.1     # ±0.1초
        self.bad_window = 0.2      # ±0.2초
        
        # 점수
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        
        # 패턴 생성
        self.generate_pattern()
    
    def generate_pattern(self):
        """리듬 패턴 생성 (리듬세상 스타일)"""
        patterns = [
            # 기본 4박자
            [1, 2, 3, 4],
            # 빠른 연타
            [1, 1.5, 2, 2.5],
            # 신코페이션
            [1, 1.75, 2.5, 3.25],
            # 복잡한 패턴
            [1, 1.25, 1.75, 2.25, 3, 3.5]
        ]
        
        current_beat = 4  # 4박자 후부터 시작
        
        for pattern_round in range(5):  # 5라운드
            pattern = random.choice(patterns)
            for beat in pattern:
                note_time = self.start_time + (current_beat + beat) * self.beat_interval
                self.notes.append(RhythmNote(note_time))
            current_beat += 6  # 각 패턴 사이에 여유
    
    def update(self, dt):
        """리듬 매니저 업데이트"""
        self.current_time = time.time()
        
        # 활성 노트 업데이트
        for note in self.active_notes[:]:
            note.update(dt, self.current_time)
            
            # 놓친 노트 처리
            if not note.is_hit and self.current_time - note.beat_time > self.bad_window:
                note.judgment = 'miss'
                note.is_hit = True
                self.combo = 0
                self.active_notes.remove(note)
        
        # 새로운 노트 활성화
        for note in self.notes[:]:
            if self.current_time >= note.beat_time - 2.0:  # 2초 전부터 활성화
                self.active_notes.append(note)
                self.notes.remove(note)
    
    def try_hit(self, hit_time=None):
        """플레이어의 입력 처리"""
        if hit_time is None:
            hit_time = self.current_time
        
        # 가장 가까운 노트 찾기
        closest_note = None
        min_distance = float('inf')
        
        for note in self.active_notes:
            if not note.is_hit:
                distance = abs(hit_time - note.beat_time)
                if distance < min_distance:
                    min_distance = distance
                    closest_note = note
        
        if closest_note is None:
            return 'miss', False
        
        # 판정 계산
        time_diff = abs(hit_time - closest_note.beat_time)
        
        if time_diff <= self.perfect_window:
            judgment = 'perfect'
            points = 300
            success = True
        elif time_diff <= self.good_window:
            judgment = 'good'
            points = 200
            success = True
        elif time_diff <= self.bad_window:
            judgment = 'bad'
            points = 100
            success = False
        else:
            judgment = 'miss'
            points = 0
            success = False
        
        # 점수 및 콤보 처리
        if success:
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            combo_bonus = min(self.combo * 10, 500)
            self.score += points + combo_bonus
        else:
            self.combo = 0
        
        # 노트 처리
        closest_note.judgment = judgment
        closest_note.is_hit = True
        if closest_note in self.active_notes:
            self.active_notes.remove(closest_note)
        
        return judgment, success
    
    def draw(self):
        """리듬 시스템 그리기"""
        # 활성 노트 그리기
        for note in self.active_notes:
            note.draw(self.current_time)
        
        # 타이밍 가이드 (중앙선)
        line_width = 3
        draw_rectangle(400 - line_width//2, 250, 400 + line_width//2, 350)
        
        # UI 정보
        self.draw_ui()
    
    def draw_ui(self):
        """UI 정보 그리기"""
        # 점수
        # 텍스트는 pico2d에서 직접 지원하지 않으므로 간단히 표시
        
        # 콤보 표시 (원으로 근사)
        if self.combo > 0:
            combo_size = min(self.combo * 2, 50)
            draw_rectangle(50 - combo_size//2, 550 - combo_size//2,
                          50 + combo_size//2, 550 + combo_size//2)
    
    def get_current_beat(self):
        """현재 박자 위치 반환"""
        elapsed = self.current_time - self.start_time
        return elapsed / self.beat_interval
    
    def is_finished(self):
        """패턴이 모두 끝났는지 확인"""
        return len(self.notes) == 0 and len(self.active_notes) == 0
