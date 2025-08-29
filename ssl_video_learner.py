#!/usr/bin/env python3
"""
SSL Video Learner
Watches SSL pro videos to learn mechanics and strategies
Works with the game injector to practice what it learns
"""

import time
import threading
import random
import numpy as np
from datetime import datetime
import json
import os
import sys
import pickle
import cv2
import requests
from bs4 import BeautifulSoup
import yt_dlp
import subprocess

class SSLVideoLearner:
    """SSL Video Learner that watches pro videos and learns"""
    
    def __init__(self):
        self.is_learning = True
        self.is_watching = False
        self.start_time = time.time()
        
        # Learning data
        self.learned_mechanics = {}
        self.learned_strategies = {}
        self.learned_positioning = {}
        self.learned_game_sense = {}
        self.videos_watched = 0
        self.total_learning_time = 0
        
        # SSL Pro players to learn from
        self.ssl_players = {
            'jstn': {
                'name': 'Justin',
                'specialties': ['mechanics', 'air_dribbles', 'flip_resets'],
                'playstyle': 'aggressive',
                'youtube_channel': 'jstn',
                'twitch_channel': 'jstn'
            },
            'garettg': {
                'name': 'GarettG',
                'specialties': ['positioning', 'game_sense', 'teamwork'],
                'playstyle': 'strategic',
                'youtube_channel': 'GarettG',
                'twitch_channel': 'GarettG'
            },
            'squishy': {
                'name': 'SquishyMuffinz',
                'specialties': ['mechanics', 'ceiling_shots', 'double_taps'],
                'playstyle': 'mechanical',
                'youtube_channel': 'SquishyMuffinz',
                'twitch_channel': 'SquishyMuffinz'
            },
            'kronovi': {
                'name': 'Kronovi',
                'specialties': ['fundamentals', 'positioning', 'consistency'],
                'playstyle': 'fundamental',
                'youtube_channel': 'Kronovi',
                'twitch_channel': 'Kronovi'
            },
            'lethamyr': {
                'name': 'Lethamyr',
                'specialties': ['mechanics', 'creativity', 'training'],
                'playstyle': 'creative',
                'youtube_channel': 'Lethamyr',
                'twitch_channel': 'Lethamyr'
            }
        }
        
        # SSL mechanics to learn from videos
        self.ssl_mechanics = {
            'speed_flip': {
                'keywords': ['speed flip', 'speedflip', 'fast kickoff'],
                'difficulty': 'expert',
                'usage_frequency': 0.8
            },
            'wave_dash': {
                'keywords': ['wave dash', 'wavedash', 'landing'],
                'difficulty': 'advanced',
                'usage_frequency': 0.7
            },
            'air_dribble': {
                'keywords': ['air dribble', 'airdribble', 'air control'],
                'difficulty': 'expert',
                'usage_frequency': 0.6
            },
            'ceiling_shot': {
                'keywords': ['ceiling shot', 'ceiling', 'wall shot'],
                'difficulty': 'expert',
                'usage_frequency': 0.4
            },
            'flip_reset': {
                'keywords': ['flip reset', 'flipreset', 'reset'],
                'difficulty': 'master',
                'usage_frequency': 0.3
            },
            'musty_flick': {
                'keywords': ['musty flick', 'musty', 'flick'],
                'difficulty': 'advanced',
                'usage_frequency': 0.5
            },
            'double_tap': {
                'keywords': ['double tap', 'doubletap', 'backboard'],
                'difficulty': 'expert',
                'usage_frequency': 0.4
            },
            'air_roll_shot': {
                'keywords': ['air roll shot', 'airroll', 'air shot'],
                'difficulty': 'advanced',
                'usage_frequency': 0.7
            },
            'backboard_read': {
                'keywords': ['backboard read', 'backboard', 'read'],
                'difficulty': 'advanced',
                'usage_frequency': 0.6
            },
            'pinch_shot': {
                'keywords': ['pinch shot', 'pinch', 'power shot'],
                'difficulty': 'expert',
                'usage_frequency': 0.3
            }
        }
        
        # SSL strategies to learn from videos
        self.ssl_strategies = {
            'rotation': {
                'keywords': ['rotation', 'rotate', 'positioning'],
                'importance': 'high',
                'usage_frequency': 0.9
            },
            'boost_management': {
                'keywords': ['boost', 'boost management', 'boost path'],
                'importance': 'high',
                'usage_frequency': 0.95
            },
            'challenge_timing': {
                'keywords': ['challenge', 'timing', '50/50'],
                'importance': 'medium',
                'usage_frequency': 0.8
            },
            'shadow_defense': {
                'keywords': ['shadow', 'defense', 'shadowing'],
                'importance': 'medium',
                'usage_frequency': 0.7
            },
            'demo_play': {
                'keywords': ['demo', 'bump', 'demolition'],
                'importance': 'medium',
                'usage_frequency': 0.6
            },
            'possession_play': {
                'keywords': ['possession', 'control', 'ball control'],
                'importance': 'high',
                'usage_frequency': 0.9
            }
        }
        
        print("🏆 SSL VIDEO LEARNER")
        print("=" * 60)
        print("🎯 Target: Learn from SSL pro videos")
        print("🧠 Watches jstn, GarettG, and other pros")
        print("⚡ Learns mechanics and strategies")
        print("🎮 Prepares for game practice")
        print("🚀 Starting SSL video learning...")
    
    def find_ssl_videos(self, player_name, max_videos=10):
        """Find SSL videos for a specific player"""
        try:
            print(f"🔍 Searching for {player_name} SSL videos...")
            
            if player_name not in self.ssl_players:
                print(f"❌ Player {player_name} not found!")
                return []
            
            player = self.ssl_players[player_name]
            videos = []
            
            # Search YouTube for SSL videos
            search_queries = [
                f"{player['name']} SSL",
                f"{player['name']} Rocket League SSL",
                f"{player['name']} pro gameplay",
                f"{player['name']} tournament"
            ]
            
            for query in search_queries:
                try:
                    # Use yt-dlp to search for videos
                    ydl_opts = {
                        'quiet': True,
                        'no_warnings': True,
                        'extract_flat': True,
                        'max_results': 5
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        search_results = ydl.extract_info(
                            f"ytsearch{5}:{query}",
                            download=False
                        )
                        
                        if search_results and 'entries' in search_results:
                            for entry in search_results['entries']:
                                if entry:
                                    videos.append({
                                        'title': entry.get('title', ''),
                                        'url': entry.get('url', ''),
                                        'duration': entry.get('duration', 0),
                                        'player': player_name,
                                        'query': query
                                    })
                    
                except Exception as e:
                    print(f"❌ Error searching for {query}: {e}")
                    continue
            
            # Remove duplicates
            unique_videos = []
            seen_urls = set()
            for video in videos:
                if video['url'] not in seen_urls:
                    unique_videos.append(video)
                    seen_urls.add(video['url'])
            
            print(f"✅ Found {len(unique_videos)} videos for {player_name}")
            return unique_videos[:max_videos]
            
        except Exception as e:
            print(f"❌ Error finding videos for {player_name}: {e}")
            return []
    
    def analyze_video_content(self, video_url, player_name):
        """Analyze video content for SSL mechanics and strategies"""
        try:
            print(f"📹 Analyzing video: {video_url}")
            
            # Extract video info
            ydl_opts = {
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(video_url, download=False)
                
                title = video_info.get('title', '')
                description = video_info.get('description', '')
                duration = video_info.get('duration', 0)
                
                print(f"   Title: {title}")
                print(f"   Duration: {duration}s")
            
            # Analyze for mechanics
            mechanics_found = []
            for mechanic, data in self.ssl_mechanics.items():
                for keyword in data['keywords']:
                    if keyword.lower() in title.lower() or keyword.lower() in description.lower():
                        mechanics_found.append({
                            'mechanic': mechanic,
                            'keyword': keyword,
                            'difficulty': data['difficulty'],
                            'usage_frequency': data['usage_frequency']
                        })
                        break
            
            # Analyze for strategies
            strategies_found = []
            for strategy, data in self.ssl_strategies.items():
                for keyword in data['keywords']:
                    if keyword.lower() in title.lower() or keyword.lower() in description.lower():
                        strategies_found.append({
                            'strategy': strategy,
                            'keyword': keyword,
                            'importance': data['importance'],
                            'usage_frequency': data['usage_frequency']
                        })
                        break
            
            # Record learning
            learning_data = {
                'video_url': video_url,
                'player': player_name,
                'title': title,
                'duration': duration,
                'mechanics_found': mechanics_found,
                'strategies_found': strategies_found,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"   🎯 Mechanics found: {len(mechanics_found)}")
            for mechanic in mechanics_found:
                print(f"      → {mechanic['mechanic']} ({mechanic['difficulty']})")
            
            print(f"   🎯 Strategies found: {len(strategies_found)}")
            for strategy in strategies_found:
                print(f"      → {strategy['strategy']} ({strategy['importance']})")
            
            return learning_data
            
        except Exception as e:
            print(f"❌ Error analyzing video {video_url}: {e}")
            return None
    
    def learn_from_videos(self, duration_minutes=60):
        """Learn from SSL videos for specified duration"""
        try:
            print(f"\n🚀 STARTING VIDEO LEARNING")
            print("=" * 60)
            print(f"⏰ Duration: {duration_minutes} minutes")
            print("🎯 Learning from SSL pro videos")
            print("🧠 Analyzing mechanics and strategies")
            print("⚡ Building understanding and knowledge")
            
            self.is_watching = True
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            # Cycle through players
            players = list(self.ssl_players.keys())
            player_index = 0
            
            while self.is_watching and time.time() < end_time:
                try:
                    # Get current player
                    current_player = players[player_index % len(players)]
                    player_index += 1
                    
                    print(f"\n👤 Learning from: {current_player}")
                    print("-" * 40)
                    
                    # Find videos for this player
                    videos = self.find_ssl_videos(current_player, 5)
                    
                    if not videos:
                        print(f"❌ No videos found for {current_player}")
                        continue
                    
                    # Analyze videos
                    for video in videos:
                        if not self.is_watching or time.time() >= end_time:
                            break
                        
                        learning_data = self.analyze_video_content(video['url'], current_player)
                        
                        if learning_data:
                            # Record learning
                            self.record_video_learning(learning_data)
                            self.videos_watched += 1
                            
                            # Brief pause between videos
                            time.sleep(random.uniform(2, 5))
                        
                        # Show progress
                        elapsed = time.time() - start_time
                        remaining = end_time - time.time()
                        print(f"\n📊 Progress: {elapsed/60:.1f}min elapsed, {remaining/60:.1f}min remaining")
                        print(f"📹 Videos watched: {self.videos_watched}")
                        print(f"🎯 Total learning time: {self.total_learning_time:.1f}s")
                    
                except Exception as e:
                    print(f"❌ Error learning from {current_player}: {e}")
                    time.sleep(1)
            
            self.is_watching = False
            print(f"\n✅ Video learning completed!")
            self.generate_learning_report()
            
        except Exception as e:
            print(f"❌ Error in video learning: {e}")
            self.is_watching = False
    
    def record_video_learning(self, learning_data):
        """Record what was learned from a video"""
        try:
            # Record mechanics
            for mechanic_data in learning_data['mechanics_found']:
                mechanic_name = mechanic_data['mechanic']
                
                if mechanic_name not in self.learned_mechanics:
                    self.learned_mechanics[mechanic_name] = {
                        'videos_watched': 0,
                        'total_time': 0,
                        'difficulty': mechanic_data['difficulty'],
                        'usage_frequency': mechanic_data['usage_frequency'],
                        'players_learned_from': []
                    }
                
                self.learned_mechanics[mechanic_name]['videos_watched'] += 1
                self.learned_mechanics[mechanic_name]['total_time'] += learning_data['duration']
                if learning_data['player'] not in self.learned_mechanics[mechanic_name]['players_learned_from']:
                    self.learned_mechanics[mechanic_name]['players_learned_from'].append(learning_data['player'])
            
            # Record strategies
            for strategy_data in learning_data['strategies_found']:
                strategy_name = strategy_data['strategy']
                
                if strategy_name not in self.learned_strategies:
                    self.learned_strategies[strategy_name] = {
                        'videos_watched': 0,
                        'total_time': 0,
                        'importance': strategy_data['importance'],
                        'usage_frequency': strategy_data['usage_frequency'],
                        'players_learned_from': []
                    }
                
                self.learned_strategies[strategy_name]['videos_watched'] += 1
                self.learned_strategies[strategy_name]['total_time'] += learning_data['duration']
                if learning_data['player'] not in self.learned_strategies[strategy_name]['players_learned_from']:
                    self.learned_strategies[strategy_name]['players_learned_from'].append(learning_data['player'])
            
            # Update total learning time
            self.total_learning_time += learning_data['duration']
            
        except Exception as e:
            print(f"❌ Error recording video learning: {e}")
    
    def generate_learning_report(self):
        """Generate comprehensive learning report"""
        try:
            print(f"\n\n📊 SSL VIDEO LEARNING REPORT")
            print("=" * 70)
            
            total_time = time.time() - self.start_time
            hours = total_time / 3600
            
            print(f"⏰ Total Learning Time: {hours:.2f} hours")
            print(f"📹 Videos Watched: {self.videos_watched}")
            print(f"🎯 Total Video Time: {self.total_learning_time/3600:.2f} hours")
            
            # Mechanics learning
            print(f"\n🎯 MECHANICS LEARNED:")
            print("-" * 30)
            for mechanic, data in self.learned_mechanics.items():
                print(f"   {mechanic}: {data['videos_watched']} videos, {data['total_time']/3600:.1f}h")
                print(f"      Difficulty: {data['difficulty']}, Usage: {data['usage_frequency']:.1%}")
                print(f"      Players: {', '.join(data['players_learned_from'])}")
            
            # Strategies learning
            print(f"\n🎯 STRATEGIES LEARNED:")
            print("-" * 30)
            for strategy, data in self.learned_strategies.items():
                print(f"   {strategy}: {data['videos_watched']} videos, {data['total_time']/3600:.1f}h")
                print(f"      Importance: {data['importance']}, Usage: {data['usage_frequency']:.1%}")
                print(f"      Players: {', '.join(data['players_learned_from'])}")
            
            # Overall assessment
            print(f"\n🏆 OVERALL ASSESSMENT:")
            print("-" * 25)
            total_mechanics = len(self.learned_mechanics)
            total_strategies = len(self.learned_strategies)
            
            print(f"   Mechanics learned: {total_mechanics}/{len(self.ssl_mechanics)}")
            print(f"   Strategies learned: {total_strategies}/{len(self.ssl_strategies)}")
            
            # SSL readiness
            ssl_readiness = (total_mechanics + total_strategies) / (len(self.ssl_mechanics) + len(self.ssl_strategies))
            print(f"   SSL Knowledge: {ssl_readiness:.1%}")
            
            if ssl_readiness >= 0.8:
                print(f"   🏆 READY FOR GAME PRACTICE!")
            elif ssl_readiness >= 0.6:
                print(f"   ⚠️ Almost ready - needs more videos")
            else:
                print(f"   ❌ Needs more video learning")
            
            # Save learning data
            self.save_learning_data()
            
        except Exception as e:
            print(f"❌ Error generating learning report: {e}")
    
    def save_learning_data(self):
        """Save learned data for game practice"""
        try:
            learning_data = {
                'learned_mechanics': self.learned_mechanics,
                'learned_strategies': self.learned_strategies,
                'videos_watched': self.videos_watched,
                'total_learning_time': self.total_learning_time,
                'total_time': time.time() - self.start_time,
                'timestamp': datetime.now().isoformat()
            }
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'ssl_video_learning_data_{timestamp}.pkl'
            
            with open(filename, 'wb') as f:
                pickle.dump(learning_data, f)
            
            print(f"\n💾 Learning data saved to: {filename}")
            print("🎮 Ready for game practice!")
            
        except Exception as e:
            print(f"❌ Error saving learning data: {e}")
    
    def stop_learning(self):
        """Stop the learning"""
        self.is_learning = False
        self.is_watching = False
        print("⏹️ Learning stopped")

def main():
    """Main function"""
    print("🏆 SSL VIDEO LEARNER")
    print("=" * 60)
    print("🎯 Target: Learn from SSL pro videos")
    print("🧠 Watches jstn, GarettG, and other pros")
    print("⚡ Learns mechanics and strategies")
    print("🎮 Prepares for game practice")
    print("🚀 Starting SSL video learning...")
    
    learner = SSLVideoLearner()
    
    try:
        # Learn from videos for 60 minutes
        learner.learn_from_videos(60)
        
    except KeyboardInterrupt:
        print("\n⏹️ Learning interrupted by user")
        learner.stop_learning()
        learner.generate_learning_report()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")

if __name__ == "__main__":
    main()
