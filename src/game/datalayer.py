import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class GameSaveManager:
    """Управление сохранениями игровых сессий"""
    
    def __init__(self, save_dir='saves'):
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.current_save_path = os.path.join(save_dir, 'autosave.json')
    
    def save_game(self, game_state: Dict, backpack=None, character=None) -> bool:
        """Сохраняет текущее состояние игры в файл"""
        try:
            # Сохраняем предметы рюкзака как JSON-совместимые данные
            backpack_data = {}
            if backpack:
                backpack_data = {
                    'weapon': [
                        {
                            'subtype': item.subtype,
                            'item_type': item.item_type,
                            'letter': item.letter,
                            'health': item.health,
                            'max_health': item.max_health,
                            'dexterity': item.dexterity,
                            'strength': item.strength,
                            'value': item.value
                        }
                        for item in backpack.get_weapons()
                    ],
                    'food': [
                        {
                            'subtype': item.subtype,
                            'item_type': item.item_type,
                            'letter': item.letter,
                            'health': item.health,
                            'max_health': item.max_health,
                            'dexterity': item.dexterity,
                            'strength': item.strength,
                            'value': item.value
                        }
                        for item in backpack.get_food()
                    ],
                    'potion': [
                        {
                            'subtype': item.subtype,
                            'item_type': item.item_type,
                            'letter': item.letter,
                            'health': item.health,
                            'max_health': item.max_health,
                            'dexterity': item.dexterity,
                            'strength': item.strength,
                            'value': item.value
                        }
                        for item in backpack.get_potions()
                    ],
                    'scroll': [
                        {
                            'subtype': item.subtype,
                            'item_type': item.item_type,
                            'letter': item.letter,
                            'health': item.health,
                            'max_health': item.max_health,
                            'dexterity': item.dexterity,
                            'strength': item.strength,
                            'value': item.value
                        }
                        for item in backpack.get_scrolls()
                    ],
                    'treasure': backpack.treasure
                }

            # Сохраняем характеристики персонажа
            character_data = game_state.get('player', {})
            if character:
                character_data = {
                    'health': character.health,
                    'max_health': character.max_health,
                    'strength': character.strength,
                    'dexterity': character.dexterity,
                    'regen_limit': character.regen_limit,
                    'x': character.x,
                    'y': character.y,
                    'cords': (character.x, character.y),
                    'level': (character.health - 30) // 10 if character.health > 40 else 1,
                    'gold': backpack.treasure if backpack else 0
                }
            
            save_data = {
                'timestamp': datetime.now().isoformat(),
                'level': game_state.get('level', 1),
                'player': character_data,
                'backpack': backpack_data,
                'enemies': game_state.get('enemies', []),
                'items': game_state.get('items', []),
                'rooms': game_state.get('rooms', []),
                'corridors': game_state.get('corridors', []),
                'message': game_state.get('message', '')
            }
            
            with open(self.current_save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f'Ошибка при сохранении игры: {e}')
            return False
    
    def load_game(self) -> Optional[Dict]:
        """Загружает сохраненное состояние игры"""
        if not os.path.exists(self.current_save_path):
            return None
        
        try:
            with open(self.current_save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            return save_data
        except Exception as e:
            print(f'Ошибка при загрузке игры: {e}')
            return None
    
    def has_save(self) -> bool:
        """Проверяет наличие сохраненной игры"""
        return os.path.exists(self.current_save_path)
    
    def delete_save(self) -> bool:
        """Удаляет сохраненную игру"""
        if os.path.exists(self.current_save_path):
            try:
                os.remove(self.current_save_path)
                return True
            except Exception as e:
                print(f'Ошибка при удалении сохранения: {e}')
                return False
        return False


class StatisticsManager:
    """Управление статистикой попыток прохождения"""
    
    def __init__(self, stats_file='stats/statistics.json'):
        self.stats_file = stats_file
        stats_dir = os.path.dirname(stats_file)
        if stats_dir and not os.path.exists(stats_dir):
            os.makedirs(stats_dir)
        self.stats = self._load_stats()
    
    def _load_stats(self) -> List[Dict]:
        """Загружает статистику из файла"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f'Ошибка при загрузке статистики: {e}')
        return []
    
    def add_attempt(self, attempt_data: Dict) -> bool:
        """Добавляет запись о попытке прохождения"""
        try:
            record = {
                'id': len(self.stats) + 1,
                'timestamp': datetime.now().isoformat(),
                'level_reached': attempt_data.get('level_reached', 1),
                'max_health': attempt_data.get('max_health', 40),
                'health': attempt_data.get('health', 40),
                'strength': attempt_data.get('strength', 15),
                'dexterity': attempt_data.get('dexterity', 6),
                'gold': attempt_data.get('gold', 0),
                'enemies_defeated': attempt_data.get('enemies_defeated', 0),
                'game_won': attempt_data.get('game_won', False),
                'play_time': attempt_data.get('play_time', 0)  # в секундах
            }
            self.stats.append(record)
            return self._save_stats()
        except Exception as e:
            print(f'Ошибка при добавлении статистики: {e}')
            return False
    
    def _save_stats(self) -> bool:
        """Сохраняет статистику в файл"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f'Ошибка при сохранении статистики: {e}')
            return False
    
    def get_all_attempts(self) -> List[Dict]:
        """Возвращает все попытки"""
        return self.stats
    
    def get_stats_summary(self) -> Dict:
        """Возвращает сводку по статистике"""
        if not self.stats:
            return {
                'total_attempts': 0,
                'max_level': 0,
                'successful_runs': 0,
                'total_enemies_defeated': 0
            }
        
        return {
            'total_attempts': len(self.stats),
            'max_level': max([s['level_reached'] for s in self.stats], default=0),
            'successful_runs': len([s for s in self.stats if s['game_won']]),
            'total_enemies_defeated': sum([s['enemies_defeated'] for s in self.stats], 0),
            'avg_gold': int(sum([s['gold'] for s in self.stats]) / len(self.stats)) if self.stats else 0
        }


class LeaderboardManager:
    """Управление таблицей лидеров"""
    
    def __init__(self, stats_manager: StatisticsManager):
        self.stats_manager = stats_manager
    
    def get_leaderboard_by_level(self, limit: int = 10) -> List[Dict]:
        """Возвращает топ попыток по максимально достигнутому уровню"""
        attempts = sorted(
            self.stats_manager.get_all_attempts(),
            key=lambda x: (-x['level_reached'], -x['gold']),
            reverse=False
        )[:limit]
        return attempts
    
    def get_leaderboard_by_gold(self, limit: int = 10) -> List[Dict]:
        """Возвращает топ попыток по накопленному золоту"""
        attempts = sorted(
            self.stats_manager.get_all_attempts(),
            key=lambda x: (-x['gold'], -x['level_reached']),
            reverse=False
        )[:limit]
        return attempts
    
    def get_leaderboard_successful(self, limit: int = 10) -> List[Dict]:
        """Возвращает успешные прохождения (уровень 21+)"""
        successful = [s for s in self.stats_manager.get_all_attempts() if s['game_won']]
        attempts = sorted(
            successful,
            key=lambda x: (x['timestamp']),
            reverse=True
        )[:limit]
        return attempts
    
    def get_player_rank_by_level(self, attempt_id: int) -> Optional[int]:
        """Возвращает ранг попытки по уровню"""
        leaderboard = self.get_leaderboard_by_level(limit=100)
        for rank, attempt in enumerate(leaderboard, 1):
            if attempt['id'] == attempt_id:
                return rank
        return None
    
    def format_leaderboard(self, leaderboard: List[Dict]) -> str:
        """Форматирует таблицу лидеров для вывода"""
        if not leaderboard:
            return 'Таблица лидеров пуста'
        
        result = 'Таблица лидеров:\n'
        result += f'{"Ранг":<5} {"Уровень":<10} {"Золото":<10} {"Дата":<20}\n'
        result += '-' * 45 + '\n'
        
        for rank, attempt in enumerate(leaderboard, 1):
            date = datetime.fromisoformat(attempt['timestamp']).strftime('%Y-%m-%d %H:%M')
            result += f'{rank:<5} {attempt["level_reached"]:<10} {attempt["gold"]:<10} {date:<20}\n'
        
        return result
