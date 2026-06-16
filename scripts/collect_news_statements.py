#!/usr/bin/env python3
"""
뉴스 및 주요 인사 발언 수집 스크립트
정치, 안보, 국제정세 관련 뉴스와 주요 인사 발언 모니터링
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import sys

class NewsAndStatementCollector:
    """뉴스 및 발언 수집 클래스"""
    
    def __init__(self):
        self.sources = {}
        self.key_figures = []
    
    def get_news_sources(self) -> Dict[str, Any]:
        """
        주요 뉴스 소스 정보
        """
        return {
            'global_financial': {
                'bloomberg': {
                    'url': 'https://www.bloomberg.com',
                    'api': 'Bloomberg API',
                    'topics': ['markets', 'economics', 'politics', 'technology'],
                    'description': '글로벌 금융 및 비즈니스 뉴스'
                },
                'reuters': {
                    'url': 'https://www.reuters.com',
                    'api': 'Reuters API',
                    'topics': ['business', 'markets', 'world', 'politics'],
                    'description': '국제 뉴스 통신사'
                },
                'ft': {
                    'url': 'https://www.ft.com',
                    'api': 'Financial Times API',
                    'topics': ['markets', 'world', 'economics'],
                    'description': 'Financial Times'
                },
                'wsj': {
                    'url': 'https://www.wsj.com',
                    'topics': ['markets', 'economy', 'politics', 'world'],
                    'description': 'Wall Street Journal'
                },
                'cnbc': {
                    'url': 'https://www.cnbc.com',
                    'api': 'CNBC API',
                    'topics': ['markets', 'investing', 'business'],
                    'description': 'CNBC Business News'
                }
            },
            'korean_financial': {
                'maeil': {
                    'url': 'https://www.mk.co.kr',
                    'description': '매일경제',
                    'topics': ['증시', '경제', '국제', '정치']
                },
                'hankyung': {
                    'url': 'https://www.hankyung.com',
                    'description': '한국경제',
                    'topics': ['증권', '금융', '경제정책']
                },
                'chosun_economy': {
                    'url': 'https://biz.chosun.com',
                    'description': '조선비즈',
                    'topics': ['증권', '경제', '국제']
                },
                'mt': {
                    'url': 'https://news.mt.co.kr',
                    'description': '머니투데이',
                    'topics': ['증권', '경제', '부동산']
                },
                'edaily': {
                    'url': 'https://www.edaily.co.kr',
                    'description': '이데일리',
                    'topics': ['증권', '산업', '경제']
                }
            },
            'geopolitical': {
                'economist': {
                    'url': 'https://www.economist.com',
                    'topics': ['politics', 'economics', 'international'],
                    'description': 'The Economist'
                },
                'foreignpolicy': {
                    'url': 'https://foreignpolicy.com',
                    'topics': ['security', 'diplomacy', 'economics'],
                    'description': 'Foreign Policy Magazine'
                },
                'stratfor': {
                    'url': 'https://worldview.stratfor.com',
                    'topics': ['geopolitics', 'security', 'economy'],
                    'description': 'Stratfor Geopolitical Analysis'
                }
            },
            'aggregators': {
                'google_news': {
                    'url': 'https://news.google.com',
                    'api': 'Google News API',
                    'description': '구글 뉴스 통합'
                },
                'newsapi': {
                    'url': 'https://newsapi.org',
                    'api': 'News API',
                    'description': '70,000+ 뉴스 소스 통합 API'
                },
                'seeking_alpha': {
                    'url': 'https://seekingalpha.com',
                    'api': 'Seeking Alpha API',
                    'description': '투자 전문 뉴스 및 분석'
                }
            }
        }
    
    def get_key_figures(self) -> Dict[str, Any]:
        """
        모니터링할 주요 인사 목록 및 소스
        """
        return {
            'us_officials': {
                'trump': {
                    'name': 'Donald Trump',
                    'position': 'US President (2025-)',
                    'sources': [
                        'Truth Social',
                        'White House statements',
                        'Press conferences',
                        'Twitter/X (@realDonaldTrump)'
                    ],
                    'topics': ['trade policy', 'tariffs', 'Fed policy', 'China relations', 'immigration'],
                    'market_impact': 'HIGH',
                    'monitoring_keywords': ['tariff', 'trade', 'China', 'Fed', 'interest rate', 'tax']
                },
                'powell': {
                    'name': 'Jerome Powell',
                    'position': 'Fed Chair',
                    'sources': [
                        'Fed press conferences',
                        'FOMC statements',
                        'Congressional testimonies'
                    ],
                    'topics': ['monetary policy', 'interest rates', 'inflation', 'employment'],
                    'market_impact': 'VERY HIGH',
                    'monitoring_keywords': ['rate', 'inflation', 'employment', 'tightening', 'easing']
                },
                'yellen': {
                    'name': 'Janet Yellen',
                    'position': 'Treasury Secretary',
                    'sources': [
                        'Treasury statements',
                        'Congressional testimonies'
                    ],
                    'topics': ['fiscal policy', 'debt ceiling', 'sanctions'],
                    'market_impact': 'HIGH',
                    'monitoring_keywords': ['fiscal', 'debt', 'sanctions', 'dollar']
                }
            },
            'tech_leaders': {
                'musk': {
                    'name': 'Elon Musk',
                    'position': 'Tesla/SpaceX/X CEO',
                    'sources': ['Twitter/X (@elonmusk)'],
                    'topics': ['tech', 'crypto', 'AI', 'EV'],
                    'market_impact': 'HIGH',
                    'monitoring_keywords': ['Tesla', 'crypto', 'Bitcoin', 'AI', 'Dogecoin']
                },
                'buffett': {
                    'name': 'Warren Buffett',
                    'position': 'Berkshire Hathaway CEO',
                    'sources': ['Berkshire letters', 'CNBC interviews', 'Annual meetings'],
                    'topics': ['value investing', 'market outlook'],
                    'market_impact': 'MEDIUM',
                    'monitoring_keywords': ['investment', 'market', 'buy', 'sell']
                }
            },
            'international': {
                'xi': {
                    'name': 'Xi Jinping',
                    'position': 'China President',
                    'sources': [
                        'Xinhua News Agency',
                        'CCTV statements',
                        'Official speeches'
                    ],
                    'topics': ['US-China relations', 'Taiwan', 'tech policy', 'economy'],
                    'market_impact': 'VERY HIGH',
                    'monitoring_keywords': ['trade', 'Taiwan', 'technology', 'US', 'decoupling']
                },
                'lagarde': {
                    'name': 'Christine Lagarde',
                    'position': 'ECB President',
                    'sources': ['ECB press conferences', 'Official statements'],
                    'topics': ['European monetary policy', 'inflation', 'Euro'],
                    'market_impact': 'HIGH',
                    'monitoring_keywords': ['rate', 'inflation', 'Euro', 'policy']
                },
                'korea_officials': {
                    'bok_governor': {
                        'name': '한국은행 총재',
                        'position': 'Bank of Korea Governor',
                        'sources': ['한국은행 보도자료', '금융통화위원회 의사록'],
                        'topics': ['기준금리', '환율', '인플레이션'],
                        'market_impact': 'HIGH (Korea)',
                        'monitoring_keywords': ['기준금리', '금리', '환율', '인플레이션', '통화정책']
                    }
                }
            }
        }
    
    def get_monitoring_schedule(self) -> Dict[str, Any]:
        """
        모니터링 일정 및 이벤트
        """
        return {
            'regular_events': {
                'fomc_meetings': {
                    'frequency': '연 8회 (6주마다)',
                    'impact': 'VERY HIGH',
                    'description': 'Fed 금리 결정 및 성명서',
                    'typical_time': '미국 동부시간 오후 2시',
                    'korean_time': '한국시간 새벽 3-4시'
                },
                'nonfarm_payrolls': {
                    'frequency': '매월 첫째주 금요일',
                    'impact': 'HIGH',
                    'description': '미국 고용지표',
                    'typical_time': '미국 동부시간 오전 8:30',
                    'korean_time': '한국시간 밤 9:30-10:30'
                },
                'cpi_release': {
                    'frequency': '매월 중순',
                    'impact': 'HIGH',
                    'description': '미국 소비자물가지수',
                    'typical_time': '미국 동부시간 오전 8:30',
                    'korean_time': '한국시간 밤 9:30-10:30'
                },
                'earnings_season': {
                    'frequency': '분기별 (1월, 4월, 7월, 10월)',
                    'impact': 'HIGH',
                    'description': '기업 실적 발표',
                    'duration': '약 4-6주'
                },
                'korea_bok_meeting': {
                    'frequency': '연 8회',
                    'impact': 'HIGH (Korea)',
                    'description': '한국은행 금융통화위원회',
                    'typical_time': '오전 10시'
                }
            },
            'search_queries': {
                'breaking_news': [
                    'breaking market news',
                    'Trump tariff announcement',
                    'Fed rate decision',
                    'geopolitical crisis',
                    'central bank policy change'
                ],
                'korean_market': [
                    '코스피 급등',
                    '코스피 급락',
                    '외국인 매수',
                    '외국인 매도',
                    '한국은행 금리'
                ],
                'sentiment_indicators': [
                    'market fear',
                    'investor sentiment',
                    'risk off',
                    'flight to safety'
                ]
            }
        }
    
    def get_collection_apis(self) -> Dict[str, Any]:
        """
        데이터 수집에 사용할 수 있는 API 목록
        """
        return {
            'news_apis': {
                'newsapi': {
                    'url': 'https://newsapi.org',
                    'free_tier': '100 requests/day',
                    'paid_tier': 'Unlimited',
                    'features': ['Keyword search', 'Source filtering', 'Date range']
                },
                'gnews': {
                    'url': 'https://gnews.io',
                    'free_tier': '100 requests/day',
                    'features': ['Google News aggregation', 'Multi-language']
                },
                'mediastack': {
                    'url': 'https://mediastack.com',
                    'free_tier': '500 requests/month',
                    'features': ['Real-time news', '50+ countries']
                }
            },
            'social_media': {
                'twitter_api': {
                    'url': 'https://developer.twitter.com',
                    'features': ['Real-time tweets', 'User timeline', 'Search'],
                    'note': 'Requires X Developer account'
                },
                'reddit_api': {
                    'url': 'https://www.reddit.com/dev/api',
                    'subreddits': [
                        'r/wallstreetbets',
                        'r/investing',
                        'r/stocks',
                        'r/options'
                    ]
                }
            },
            'financial_data': {
                'alpha_vantage': {
                    'url': 'https://www.alphavantage.co',
                    'features': ['Stock data', 'Economic indicators', 'News sentiment'],
                    'free_tier': '25 requests/day'
                },
                'finnhub': {
                    'url': 'https://finnhub.io',
                    'features': ['Market news', 'Company news', 'Press releases'],
                    'free_tier': '60 requests/minute'
                }
            }
        }
    
    def print_collection_guide(self):
        """수집 가이드 출력"""
        print("=" * 80)
        print("뉴스 및 주요 인사 발언 수집 가이드")
        print("=" * 80)
        
        # 뉴스 소스
        print("\n[주요 뉴스 소스]")
        print("-" * 80)
        sources = self.get_news_sources()
        for category, items in sources.items():
            print(f"\n{category.upper()}:")
            for key, info in items.items():
                print(f"  - {key}: {info['description']}")
                print(f"    URL: {info['url']}")
        
        # 주요 인사
        print("\n\n[모니터링 대상 주요 인사]")
        print("-" * 80)
        figures = self.get_key_figures()
        for category, people in figures.items():
            print(f"\n{category.upper()}:")
            for key, person in people.items():
                if isinstance(person, dict) and 'name' in person:
                    print(f"  - {person['name']} ({person['position']})")
                    print(f"    시장 영향도: {person['market_impact']}")
                    print(f"    모니터링 키워드: {', '.join(person['monitoring_keywords'])}")
        
        # 모니터링 일정
        print("\n\n[주요 경제 일정]")
        print("-" * 80)
        schedule = self.get_monitoring_schedule()
        for event, info in schedule['regular_events'].items():
            print(f"\n  {event}:")
            print(f"    빈도: {info['frequency']}")
            print(f"    영향도: {info['impact']}")
            print(f"    설명: {info['description']}")
        
        # API 정보
        print("\n\n[사용 가능한 API]")
        print("-" * 80)
        apis = self.get_collection_apis()
        for category, items in apis.items():
            print(f"\n{category.upper()}:")
            for key, info in items.items():
                print(f"  - {key}")
                print(f"    URL: {info['url']}")
                if 'free_tier' in info:
                    print(f"    무료: {info['free_tier']}")
        
        print("\n" + "=" * 80)

def main():
    """메인 실행 함수"""
    collector = NewsAndStatementCollector()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        # JSON 형식으로 출력
        data = {
            'news_sources': collector.get_news_sources(),
            'key_figures': collector.get_key_figures(),
            'monitoring_schedule': collector.get_monitoring_schedule(),
            'apis': collector.get_collection_apis()
        }
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        # 사람이 읽기 쉬운 형식으로 출력
        collector.print_collection_guide()

if __name__ == "__main__":
    main()
