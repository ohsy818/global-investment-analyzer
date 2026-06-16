#!/usr/bin/env python3
"""
기술적 분석 및 매매 신호 생성 스크립트
주식, ETF, 레버리지, 인버스 매매 타이밍 분석
"""

import json
from typing import Dict, List, Any, Tuple
from datetime import datetime
import sys

class TradingSignalGenerator:
    """매매 신호 생성 클래스"""
    
    def __init__(self):
        self.indicators = {}
        self.strategies = {}
    
    def get_technical_indicators(self) -> Dict[str, Any]:
        """
        기술적 지표 목록 및 설명
        """
        return {
            'trend_indicators': {
                'moving_averages': {
                    'ma5': '5일 이동평균선 - 단기 추세',
                    'ma20': '20일 이동평균선 - 중기 추세',
                    'ma60': '60일 이동평균선 - 장기 추세',
                    'ma120': '120일 이동평균선 - 초장기 추세',
                    'ema12': '12일 지수이동평균',
                    'ema26': '26일 지수이동평균',
                    'golden_cross': '골든크로스 (단기선이 장기선을 상향돌파)',
                    'dead_cross': '데드크로스 (단기선이 장기선을 하향돌파)',
                    'usage': 'pandas의 rolling().mean() 또는 ta-lib의 SMA/EMA'
                },
                'macd': {
                    'description': 'MACD (Moving Average Convergence Divergence)',
                    'components': {
                        'macd_line': 'EMA12 - EMA26',
                        'signal_line': 'MACD의 9일 EMA',
                        'histogram': 'MACD - Signal'
                    },
                    'buy_signal': 'MACD가 Signal을 상향돌파',
                    'sell_signal': 'MACD가 Signal을 하향돌파',
                    'usage': 'ta-lib의 MACD() 또는 pandas로 직접 계산'
                }
            },
            'momentum_indicators': {
                'rsi': {
                    'description': 'RSI (Relative Strength Index)',
                    'period': '일반적으로 14일',
                    'oversold': '30 이하 - 과매도, 매수 고려',
                    'overbought': '70 이상 - 과매수, 매도 고려',
                    'divergence': 'RSI와 가격의 다이버전스',
                    'usage': 'ta-lib의 RSI() 또는 직접 계산'
                },
                'stochastic': {
                    'description': 'Stochastic Oscillator',
                    'components': {
                        '%K': '빠른선 (5일)',
                        '%D': '느린선 (%K의 3일 이동평균)'
                    },
                    'oversold': '20 이하',
                    'overbought': '80 이상',
                    'signal': '%K가 %D를 돌파',
                    'usage': 'ta-lib의 STOCH()'
                }
            },
            'volatility_indicators': {
                'bollinger_bands': {
                    'description': '볼린저 밴드',
                    'components': {
                        'upper': '중간선 + (2 × 표준편차)',
                        'middle': '20일 이동평균',
                        'lower': '중간선 - (2 × 표준편차)'
                    },
                    'buy_signal': '하단 밴드 접근 또는 돌파',
                    'sell_signal': '상단 밴드 접근 또는 돌파',
                    'squeeze': '밴드 폭 좁아짐 → 큰 변동성 예고',
                    'usage': 'ta-lib의 BBANDS()'
                },
                'atr': {
                    'description': 'ATR (Average True Range)',
                    'purpose': '변동성 측정, 손절/익절 설정',
                    'period': '일반적으로 14일',
                    'usage': 'ta-lib의 ATR()'
                }
            },
            'volume_indicators': {
                'obv': {
                    'description': 'OBV (On-Balance Volume)',
                    'purpose': '거래량 기반 추세 확인',
                    'signal': 'OBV 추세와 가격 추세의 일치/불일치',
                    'usage': 'ta-lib의 OBV()'
                },
                'volume_analysis': {
                    'high_volume_breakout': '높은 거래량 동반 돌파',
                    'low_volume_pullback': '낮은 거래량 조정',
                    'climax_volume': '극단적 거래량 (반전 신호)'
                }
            }
        }
    
    def get_trading_strategies(self) -> Dict[str, Any]:
        """
        매매 전략 목록
        """
        return {
            'domestic_stocks': {
                'trend_following': {
                    'description': '추세 추종 전략',
                    'conditions': {
                        'buy': [
                            'MA5 > MA20 > MA60 (상승 정렬)',
                            'MACD > Signal',
                            'RSI 40-70 사이',
                            '거래량 증가'
                        ],
                        'sell': [
                            'MA5 < MA20 (데드크로스)',
                            'MACD < Signal',
                            'RSI < 30 또는 > 80'
                        ]
                    },
                    '적합종목': '대형주, 우량주',
                    'risk_management': {
                        'stop_loss': '매수가 대비 -7%',
                        'take_profit': '매수가 대비 +15%',
                        'trailing_stop': 'ATR의 2배'
                    }
                },
                'mean_reversion': {
                    'description': '평균 회귀 전략',
                    'conditions': {
                        'buy': [
                            'RSI < 30 (과매도)',
                            '볼린저 하단 접근',
                            'Stochastic < 20',
                            '지지선 근처'
                        ],
                        'sell': [
                            'RSI > 70 (과매수)',
                            '볼린저 상단 접근',
                            '저항선 근처'
                        ]
                    },
                    '적합종목': '중소형주, 변동성 큰 종목',
                    'risk_management': {
                        'stop_loss': '-5%',
                        'take_profit': '+10%'
                    }
                }
            },
            'us_stocks': {
                'growth_momentum': {
                    'description': '성장주 모멘텀 전략',
                    'screening': [
                        'EPS 성장률 > 20%',
                        '매출 성장률 > 15%',
                        '52주 신고가 근처',
                        '상대강도 상위 20%'
                    ],
                    'entry': [
                        '신고가 돌파',
                        '거래량 급증',
                        'RSI 50-70'
                    ],
                    'sectors': ['Technology', 'Healthcare', 'Consumer Discretionary']
                },
                'value_investing': {
                    'description': '가치 투자 전략',
                    'screening': [
                        'P/E < 업종 평균',
                        'P/B < 2',
                        '배당수익률 > 3%',
                        '부채비율 < 50%'
                    ],
                    'entry': [
                        '주가 52주 저점 대비 +10% 이내',
                        'RSI < 40',
                        '악재로 인한 과매도'
                    ]
                }
            },
            'etf_strategies': {
                'index_etf': {
                    'description': '인덱스 ETF 전략',
                    'products': {
                        'korea': ['KODEX 200', 'TIGER 200', 'KODEX 코스닥150'],
                        'us': ['SPY (S&P500)', 'QQQ (Nasdaq100)', 'DIA (Dow)']
                    },
                    'strategy': '장기 적립식 투자',
                    'timing': {
                        'strong_buy': '시장 조정 10% 이상 하락',
                        'buy': 'MA60 근처 지지',
                        'hold': '상승 추세',
                        'reduce': 'RSI > 75, 과열 국면'
                    }
                },
                'sector_rotation': {
                    'description': '섹터 로테이션 전략',
                    'sectors': {
                        'early_cycle': ['금융', '부동산', '소재'],
                        'mid_cycle': ['산업재', '기술', '경기소비재'],
                        'late_cycle': ['에너지', '필수소비재'],
                        'recession': ['유틸리티', '헬스케어', '채권']
                    },
                    'indicators': [
                        'GDP 성장률',
                        '제조업 PMI',
                        '수익률곡선',
                        '실업률'
                    ]
                }
            },
            'leverage_inverse': {
                'leverage_etf': {
                    'description': '레버리지 ETF (2배, 3배)',
                    'products': {
                        'korea': [
                            'KODEX 레버리지 (코스피200 2배)',
                            'TIGER 코스닥150레버리지',
                            'KODEX 미국S&P500레버리지(합성)'
                        ],
                        'us': [
                            'TQQQ (Nasdaq 3배)',
                            'UPRO (S&P500 3배)',
                            'SOXL (반도체 3배)'
                        ]
                    },
                    'when_to_use': {
                        'ideal': '강한 상승 추세 확인 후',
                        'conditions': [
                            'MA5 > MA20 > MA60',
                            'MACD 강세',
                            'RSI 50-65',
                            'VIX < 20 (낮은 변동성)'
                        ],
                        'avoid': [
                            '횡보장',
                            '약세장',
                            'VIX > 30 (고변동성)'
                        ]
                    },
                    'risk_management': {
                        'position_size': '포트폴리오의 10-20% 이하',
                        'holding_period': '단기 (1주-1개월)',
                        'stop_loss': '-10% (일반 ETF보다 빡빡하게)',
                        'monitoring': '일일 모니터링 필수'
                    },
                    'warnings': [
                        '장기 보유 시 복리 효과로 손실 확대',
                        '변동성 높음',
                        '거래 비용 높음'
                    ]
                },
                'inverse_etf': {
                    'description': '인버스 ETF (하락 시 수익)',
                    'products': {
                        'korea': [
                            'KODEX 인버스 (코스피200 -1배)',
                            'TIGER 코스닥150인버스',
                            'KODEX 미국S&P500인버스(합성)'
                        ],
                        'us': [
                            'SQQQ (Nasdaq -3배)',
                            'SPXU (S&P500 -3배)',
                            'SOXS (반도체 -3배)'
                        ]
                    },
                    'when_to_use': {
                        'ideal': '하락 추세 확실 시',
                        'conditions': [
                            'MA5 < MA20 < MA60 (하락 정렬)',
                            'MACD 약세',
                            'RSI < 50',
                            'VIX > 25 (공포 지수 상승)',
                            '경기침체 신호'
                        ],
                        'entry_signals': [
                            '주요 지지선 붕괴',
                            '데드크로스',
                            '거래량 동반 급락'
                        ]
                    },
                    'risk_management': {
                        'position_size': '포트폴리오의 5-15%',
                        'holding_period': '단기 (며칠-2주)',
                        'stop_loss': '-8%',
                        'take_profit': '+15-20%'
                    },
                    'hedge_use': '보유 주식 헷지용으로 활용'
                }
            }
        }
    
    def get_macro_signals(self) -> Dict[str, Any]:
        """
        거시경제 신호 기반 전략
        """
        return {
            'bull_market_signals': {
                'conditions': [
                    'GDP 성장률 > 2%',
                    '실업률 하락',
                    'PMI > 50',
                    '기업 실적 개선',
                    '금리 인하 또는 안정'
                ],
                'strategy': {
                    'stocks': '공격적 매수 (성장주, 기술주)',
                    'etf': '레버리지 ETF 고려',
                    'sectors': '기술, 소비재, 금융',
                    'risk_on': True
                }
            },
            'bear_market_signals': {
                'conditions': [
                    'GDP 마이너스 성장',
                    '실업률 급등',
                    'PMI < 45',
                    '기업 실적 악화',
                    '금리 급등',
                    '수익률곡선 역전'
                ],
                'strategy': {
                    'stocks': '방어적 (현금 비중 확대)',
                    'etf': '인버스 ETF, 채권 ETF',
                    'sectors': '헬스케어, 유틸리티, 필수소비재',
                    'risk_off': True
                }
            },
            'geopolitical_risk': {
                'events': [
                    '전쟁, 분쟁',
                    '무역 전쟁',
                    '정치적 불안',
                    '제재'
                ],
                'immediate_action': [
                    '안전자산 선호 (금, 달러, 국채)',
                    '인버스 ETF 매수 고려',
                    '변동성 ETF (UVXY)',
                    '리스크 자산 비중 축소'
                ],
                'sectors_to_avoid': ['항공', '관광', '신흥시장'],
                'safe_havens': ['금 ETF', '달러', '미국 국채', '방어주']
            },
            'fed_policy_impact': {
                'rate_hike_cycle': {
                    'early_stage': {
                        'impact': '주식 양호, 경기 호황',
                        'strategy': '주식 보유, 금융주 유리'
                    },
                    'mid_stage': {
                        'impact': '변동성 증가',
                        'strategy': '방어적 전환 시작'
                    },
                    'late_stage': {
                        'impact': '경기둔화 우려',
                        'strategy': '인버스 고려, 채권 비중 확대'
                    }
                },
                'rate_cut_cycle': {
                    'initial_cuts': {
                        'impact': '경기둔화 반영, 단기 하락 가능',
                        'strategy': '저점 매수 기회 준비'
                    },
                    'sustained_cuts': {
                        'impact': '유동성 공급, 주가 상승',
                        'strategy': '레버리지 ETF, 성장주 매수'
                    }
                }
            }
        }
    
    def get_risk_management_rules(self) -> Dict[str, Any]:
        """
        리스크 관리 규칙
        """
        return {
            'position_sizing': {
                'single_stock': '포트폴리오의 5-10%',
                'sector': '포트폴리오의 20-30%',
                'leverage_etf': '포트폴리오의 10-20%',
                'inverse_etf': '포트폴리오의 5-15%',
                'cash_reserve': '최소 10-20% 현금 보유'
            },
            'stop_loss_rules': {
                'stocks': {
                    'normal': '-7% 손절',
                    'tight': '-5% (변동성 큰 종목)',
                    'loose': '-10% (우량주)'
                },
                'etf': {
                    'index': '-10%',
                    'leverage': '-10% (빠르게)',
                    'inverse': '-8%'
                },
                'trailing_stop': 'ATR 기반 또는 최고점 대비 -10%'
            },
            'take_profit_rules': {
                'conservative': '+10-15%',
                'moderate': '+20-30%',
                'aggressive': '+50% 이상',
                'partial_profit': [
                    '+10% 도달 시 30% 익절',
                    '+20% 도달 시 추가 30% 익절',
                    '나머지 trailing stop'
                ]
            },
            'portfolio_rebalancing': {
                'frequency': '월 1회 또는 분기 1회',
                'conditions': [
                    '특정 종목이 목표 비중 ±5% 벗어날 때',
                    '시장 상황 변화 (강세↔약세 전환)'
                ],
                'method': '초과 수익 종목 일부 익절, 저평가 종목 추가 매수'
            },
            'emotional_discipline': {
                'rules': [
                    '사전에 정한 규칙을 따를 것',
                    'FOMO(Fear Of Missing Out) 경계',
                    '손실 시 복수 매매 금지',
                    '일일 손실 한도 설정 (-3% 이상 시 당일 거래 중단)',
                    '투자 일지 작성'
                ]
            }
        }
    
    def print_strategy_guide(self):
        """전략 가이드 출력"""
        print("=" * 80)
        print("매매 전략 및 신호 생성 가이드")
        print("=" * 80)
        
        # 기술적 지표
        print("\n[기술적 지표]")
        print("-" * 80)
        indicators = self.get_technical_indicators()
        for category, items in indicators.items():
            print(f"\n{category.upper()}:")
            for key, info in items.items():
                if isinstance(info, dict):
                    print(f"  {key}:")
                    if 'description' in info:
                        print(f"    {info['description']}")
                else:
                    print(f"  {key}: {info}")
        
        # 매매 전략
        print("\n\n[매매 전략]")
        print("-" * 80)
        strategies = self.get_trading_strategies()
        for market, strats in strategies.items():
            print(f"\n{market.upper()}:")
            for strat_name, strat_info in strats.items():
                print(f"  - {strat_name}: {strat_info.get('description', '')}")
        
        # 거시경제 신호
        print("\n\n[거시경제 신호]")
        print("-" * 80)
        macro = self.get_macro_signals()
        for signal_type, info in macro.items():
            print(f"\n{signal_type}:")
            if 'conditions' in info:
                print(f"  조건: {', '.join(info['conditions'][:3])}")
        
        # 리스크 관리
        print("\n\n[리스크 관리]")
        print("-" * 80)
        risk = self.get_risk_management_rules()
        print("\n포지션 크기:")
        for key, value in risk['position_sizing'].items():
            print(f"  - {key}: {value}")
        
        print("\n손절 규칙:")
        for category, rules in risk['stop_loss_rules'].items():
            print(f"  {category}: {rules if isinstance(rules, str) else rules.get('normal', '')}")
        
        print("\n" + "=" * 80)
        print("Python 라이브러리:")
        print("  - pandas: 데이터 처리")
        print("  - ta-lib: 기술적 지표 계산")
        print("  - yfinance: 주가 데이터 다운로드")
        print("  - mplfinance: 차트 생성")
        print("=" * 80)

def main():
    """메인 실행 함수"""
    generator = TradingSignalGenerator()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        # JSON 형식으로 출력
        data = {
            'technical_indicators': generator.get_technical_indicators(),
            'trading_strategies': generator.get_trading_strategies(),
            'macro_signals': generator.get_macro_signals(),
            'risk_management': generator.get_risk_management_rules()
        }
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        # 사람이 읽기 쉬운 형식으로 출력
        generator.print_strategy_guide()

if __name__ == "__main__":
    main()
