#!/usr/bin/env python3
"""
경제 지표 수집 스크립트
글로벌 경제 지표를 여러 소스에서 수집
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import sys

class EconomicIndicatorCollector:
    """주요 경제 지표 수집 클래스"""
    
    def __init__(self):
        self.indicators = {}
        self.sources = {
            'fred': 'Federal Reserve Economic Data',
            'investing': 'Investing.com',
            'tradingeconomics': 'Trading Economics',
            'yahoo': 'Yahoo Finance'
        }
    
    def get_us_indicators(self) -> Dict[str, Any]:
        """
        미국 경제 지표 수집
        - GDP 성장률
        - 실업률
        - 인플레이션 (CPI, PCE)
        - 연방기금금리
        - 국채 수익률 (2년, 10년)
        """
        return {
            'gdp_growth': {
                'source': 'FRED API',
                'endpoint': 'https://api.stlouisfed.org/fred/series/observations',
                'series_id': 'GDP',
                'description': 'Real GDP'
            },
            'unemployment': {
                'source': 'FRED API',
                'endpoint': 'https://api.stlouisfed.org/fred/series/observations',
                'series_id': 'UNRATE',
                'description': 'Unemployment Rate'
            },
            'cpi': {
                'source': 'FRED API',
                'endpoint': 'https://api.stlouisfed.org/fred/series/observations',
                'series_id': 'CPIAUCSL',
                'description': 'Consumer Price Index'
            },
            'fed_rate': {
                'source': 'FRED API',
                'endpoint': 'https://api.stlouisfed.org/fred/series/observations',
                'series_id': 'FEDFUNDS',
                'description': 'Federal Funds Rate'
            },
            'treasury_2y': {
                'source': 'FRED API',
                'endpoint': 'https://api.stlouisfed.org/fred/series/observations',
                'series_id': 'DGS2',
                'description': '2-Year Treasury Rate'
            },
            'treasury_10y': {
                'source': 'FRED API',
                'endpoint': 'https://api.stlouisfed.org/fred/series/observations',
                'series_id': 'DGS10',
                'description': '10-Year Treasury Rate'
            },
            'vix': {
                'source': 'Yahoo Finance',
                'ticker': '^VIX',
                'description': 'VIX Volatility Index'
            }
        }
    
    def get_korea_indicators(self) -> Dict[str, Any]:
        """
        한국 경제 지표 수집
        - GDP 성장률
        - 실업률
        - 소비자물가지수
        - 기준금리
        - KOSPI, KOSDAQ
        - 환율 (USD/KRW)
        """
        return {
            'korea_gdp': {
                'source': '한국은행 경제통계시스템',
                'endpoint': 'https://ecos.bok.or.kr/api/StatisticSearch/{api_key}/{response_type}/{lang}/{start_count}/{end_count}/{stat_code}/',
                'api_key_placeholder': 'sample',
                'response_type': 'xml',
                'lang': 'kr',
                'start_count': 1,
                'end_count': 10,
                'stat_code': '200Y104',
                'description': 'Korea Real GDP (seasonally adjusted, quarterly)'
            },
            'korea_cpi': {
                'source': '한국은행',
                'endpoint': 'https://ecos.bok.or.kr/api/StatisticSearch/{api_key}/{response_type}/{lang}/{start_count}/{end_count}/{stat_code}/',
                'api_key_placeholder': 'sample',
                'response_type': 'xml',
                'lang': 'kr',
                'start_count': 1,
                'end_count': 10,
                'stat_code': '901Y009',
                'description': 'Korea Consumer Price Index'
            },
            'korea_rate': {
                'source': '한국은행',
                'endpoint': 'https://ecos.bok.or.kr/api/StatisticSearch/{api_key}/{response_type}/{lang}/{start_count}/{end_count}/{stat_code}/',
                'api_key_placeholder': 'sample',
                'response_type': 'xml',
                'lang': 'kr',
                'start_count': 1,
                'end_count': 10,
                'stat_code': '722Y001',
                'description': 'Korea Base Rate'
            },
            'kospi': {
                'source': 'Yahoo Finance / Investing.com',
                'ticker': '^KS11',
                'description': 'KOSPI Index'
            },
            'kosdaq': {
                'source': 'Yahoo Finance / Investing.com',
                'ticker': '^KQ11',
                'description': 'KOSDAQ Index'
            },
            'usd_krw': {
                'source': 'Yahoo Finance',
                'ticker': 'KRW=X',
                'description': 'USD/KRW Exchange Rate'
            }
        }
    
    def get_global_indicators(self) -> Dict[str, Any]:
        """
        글로벌 지표 수집
        - 주요 지수 (S&P500, Nasdaq, Dow, 상해종합, 니케이)
        - 원자재 (금, 유가, 구리)
        - 달러 인덱스
        - 비트코인
        """
        return {
            'sp500': {
                'source': 'Yahoo Finance',
                'ticker': '^GSPC',
                'description': 'S&P 500 Index'
            },
            'nasdaq': {
                'source': 'Yahoo Finance',
                'ticker': '^IXIC',
                'description': 'Nasdaq Composite'
            },
            'dow': {
                'source': 'Yahoo Finance',
                'ticker': '^DJI',
                'description': 'Dow Jones Industrial Average'
            },
            'shanghai': {
                'source': 'Yahoo Finance',
                'ticker': '000001.SS',
                'description': 'Shanghai Composite'
            },
            'nikkei': {
                'source': 'Yahoo Finance',
                'ticker': '^N225',
                'description': 'Nikkei 225'
            },
            'gold': {
                'source': 'Yahoo Finance',
                'ticker': 'GC=F',
                'description': 'Gold Futures'
            },
            'crude_oil': {
                'source': 'Yahoo Finance',
                'ticker': 'CL=F',
                'description': 'Crude Oil WTI Futures'
            },
            'copper': {
                'source': 'Yahoo Finance',
                'ticker': 'HG=F',
                'description': 'Copper Futures'
            },
            'dxy': {
                'source': 'Investing.com',
                'ticker': 'DX-Y.NYB',
                'description': 'US Dollar Index'
            },
            'bitcoin': {
                'source': 'Yahoo Finance',
                'ticker': 'BTC-USD',
                'description': 'Bitcoin USD'
            }
        }
    
    def get_all_indicators(self) -> Dict[str, Dict[str, Any]]:
        """모든 지표 정보 통합 반환"""
        return {
            'us_indicators': self.get_us_indicators(),
            'korea_indicators': self.get_korea_indicators(),
            'global_indicators': self.get_global_indicators()
        }
    
    def print_collection_guide(self):
        """지표 수집 가이드 출력"""
        all_indicators = self.get_all_indicators()
        
        print("=" * 80)
        print("경제 지표 수집 가이드")
        print("=" * 80)
        
        for category, indicators in all_indicators.items():
            print(f"\n[{category.upper()}]")
            print("-" * 80)
            for key, info in indicators.items():
                print(f"\n  {key}:")
                print(f"    설명: {info['description']}")
                print(f"    출처: {info['source']}")
                if 'endpoint' in info:
                    print(f"    API: {info['endpoint']}")
                if 'ticker' in info:
                    print(f"    Ticker: {info['ticker']}")
                if 'series_id' in info:
                    print(f"    Series ID: {info['series_id']}")
        
        print("\n" + "=" * 80)
        print("API 키 필요 사항:")
        print("=" * 80)
        print("1. FRED API: https://fred.stlouisfed.org/docs/api/api_key.html")
        print("2. 한국은행: https://ecos.bok.or.kr/api/")
        print("3. Alpha Vantage: https://www.alphavantage.co/support/#api-key")
        print("=" * 80)

def main():
    """메인 실행 함수"""
    collector = EconomicIndicatorCollector()

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        # JSON 형식으로 출력
        print(json.dumps(collector.get_all_indicators(), indent=2, ensure_ascii=False))
    else:
        # 사람이 읽기 쉬운 형식으로 출력
        collector.print_collection_guide()

if __name__ == "__main__":
    main()
