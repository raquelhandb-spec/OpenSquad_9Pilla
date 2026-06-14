#!/usr/bin/env python3
"""
🔥 PROFIT FLOW ANALYZER — Processa Order Flow do Profit Pro
Lê CSVs exportados, identifica ponta, cria cenários dinâmicos
"""

import os
import csv
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Any

class ProfitFlowAnalyzer:
    """Analisa Order Flow a partir de CSVs do Profit Pro"""

    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.data = []
        self.timestamps = []
        self.prices_open = []
        self.prices_close = []
        self.volumes = []
        self.flow_balance = []

    def load_csv(self) -> bool:
        """Carrega dados do CSV exportado do Profit Pro"""

        print(f"\n📥 Carregando dados de {self.csv_file}...")

        if not os.path.exists(self.csv_file):
            print(f"❌ Arquivo não encontrado: {self.csv_file}")
            return False

        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.data.append(row)

            print(f"✅ {len(self.data)} linhas carregadas")
            return True

        except Exception as e:
            print(f"❌ Erro ao ler CSV: {e}")
            return False

    def analyze_order_flow(self) -> Dict[str, Any]:
        """Analisa o fluxo de ordens (compras vs vendas)"""

        if not self.data:
            return {}

        print("\n🔍 Analisando Order Flow...")

        # Processar cada barra
        total_compras = 0
        total_vendas = 0
        maior_compra = 0
        maior_venda = 0
        fluxo_por_barra = []

        for i, row in enumerate(self.data):
            try:
                # Extrair dados
                open_price = float(row.get('Abertura', row.get('Open', 0)))
                close_price = float(row.get('Fechamento', row.get('Close', 0)))
                volume = float(row.get('Volume', 0))
                timestamp = row.get('Data', row.get('Date', '')) + ' ' + row.get('Hora', row.get('Time', ''))

                # Determinar se foi compra ou venda
                if close_price > open_price:
                    # Preço subiu = COMPRA
                    total_compras += volume
                    maior_compra = max(maior_compra, volume)
                    tipo = "COMPRA"
                elif close_price < open_price:
                    # Preço caiu = VENDA
                    total_vendas += volume
                    maior_venda = max(maior_venda, volume)
                    tipo = "VENDA"
                else:
                    tipo = "DOJI"

                # Calcular saldo
                saldo = total_compras - total_vendas

                fluxo_por_barra.append({
                    'timestamp': timestamp,
                    'tipo': tipo,
                    'volume': volume,
                    'open': open_price,
                    'close': close_price,
                    'compras_acum': total_compras,
                    'vendas_acum': total_vendas,
                    'saldo': saldo,
                })

            except Exception as e:
                print(f"⚠️ Erro ao processar linha {i}: {e}")
                continue

        # Análise final
        saldo_final = total_compras - total_vendas
        percentual_compras = (total_compras / (total_compras + total_vendas) * 100) if (total_compras + total_vendas) > 0 else 0

        return {
            'total_compras': total_compras,
            'total_vendas': total_vendas,
            'saldo_final': saldo_final,
            'percentual_compras': percentual_compras,
            'percentual_vendas': 100 - percentual_compras,
            'maior_compra': maior_compra,
            'maior_venda': maior_venda,
            'fluxo_por_barra': fluxo_por_barra,
        }

    def identify_ponta(self, analysis: Dict) -> Dict[str, str]:
        """Identifica qual ponta está no controle"""

        saldo = analysis.get('saldo_final', 0)
        comp_pct = analysis.get('percentual_compras', 0)
        venda_pct = analysis.get('percentual_vendas', 0)

        interpretation = {}

        if saldo > 0:
            dominancia = (comp_pct - 50) * 2  # 0-100
            interpretation['ponta_controle'] = f"🔴 PONTA COMPRADORA ({comp_pct:.1f}%)"
            interpretation['forca'] = "FORTE" if dominancia > 75 else "MODERADA" if dominancia > 50 else "FRACA"
            interpretation['poder'] = f"Poder de compra: {dominancia:.0f}%"
        elif saldo < 0:
            dominancia = (venda_pct - 50) * 2
            interpretation['ponta_controle'] = f"🔵 PONTA VENDEDORA ({venda_pct:.1f}%)"
            interpretation['forca'] = "FORTE" if dominancia > 75 else "MODERADA" if dominancia > 50 else "FRACA"
            interpretation['poder'] = f"Poder de venda: {dominancia:.0f}%"
        else:
            interpretation['ponta_controle'] = f"⚖️ EQUILIBRIO DE FORÇAS"
            interpretation['forca'] = "NEUTRAL"
            interpretation['poder'] = "Sem dominância clara"

        return interpretation

    def detect_ponta_changes(self, flow_data: List[Dict]) -> List[Dict[str, str]]:
        """Detecta mudanças de controle de ponta"""

        changes = []

        if len(flow_data) < 2:
            return changes

        for i in range(1, len(flow_data)):
            saldo_atual = flow_data[i]['saldo']
            saldo_anterior = flow_data[i-1]['saldo']

            # Cruzamento: vendedora para compradora
            if saldo_anterior < 0 and saldo_atual > 0:
                changes.append({
                    'timestamp': flow_data[i]['timestamp'],
                    'tipo': '🔄 INVERSÃO',
                    'descricao': 'Ponta vendedora perdeu controle → Ponta compradora assumiu!',
                    'sinal': 'POTENCIAL COMPRA',
                })

            # Cruzamento: compradora para vendedora
            elif saldo_anterior > 0 and saldo_atual < 0:
                changes.append({
                    'timestamp': flow_data[i]['timestamp'],
                    'tipo': '🔄 INVERSÃO',
                    'descricao': 'Ponta compradora perdeu controle → Ponta vendedora assumiu!',
                    'sinal': 'POTENCIAL VENDA',
                })

            # Grande candle de compra
            elif flow_data[i]['tipo'] == 'COMPRA' and flow_data[i]['volume'] > flow_data[i-1]['volume'] * 2:
                changes.append({
                    'timestamp': flow_data[i]['timestamp'],
                    'tipo': '🔴 GRANDE COMPRA',
                    'descricao': f"Volume {flow_data[i]['volume']:.0f} — Ponta compradora ataca!",
                    'sinal': 'ALERTA DE COMPRA',
                })

            # Grande candle de venda
            elif flow_data[i]['tipo'] == 'VENDA' and flow_data[i]['volume'] > flow_data[i-1]['volume'] * 2:
                changes.append({
                    'timestamp': flow_data[i]['timestamp'],
                    'tipo': '🔵 GRANDE VENDA',
                    'descricao': f"Volume {flow_data[i]['volume']:.0f} — Ponta vendedora ataca!",
                    'sinal': 'ALERTA DE VENDA',
                })

        return changes

    def build_flow_scenario(self, analysis: Dict, ponta_info: Dict) -> str:
        """Constrói cenário dinâmico baseado no fluxo"""

        saldo = analysis.get('saldo_final', 0)
        comp_pct = analysis.get('percentual_compras', 0)

        scenario = f"""
        🎯 CENÁRIO BASEADO EM ORDER FLOW
        ════════════════════════════════════════════════════════

        {ponta_info.get('ponta_controle', '')}
        Força: {ponta_info.get('forca', '')}
        {ponta_info.get('poder', '')}

        Análise:
        • Total de compras: {analysis.get('total_compras', 0):.0f} contratos
        • Total de vendas: {analysis.get('total_vendas', 0):.0f} contratos
        • Saldo (Compras - Vendas): {saldo:.0f} contratos
        • Proporção: {comp_pct:.1f}% compras vs {analysis.get('percentual_vendas', 0):.1f}% vendas

        Maior ordem:
        • Compra máxima: {analysis.get('maior_compra', 0):.0f} contratos
        • Venda máxima: {analysis.get('maior_venda', 0):.0f} contratos

        ════════════════════════════════════════════════════════
        """

        return scenario

    def print_report(self):
        """Imprime relatório completo"""

        if not self.load_csv():
            return

        # Análise
        analysis = self.analyze_order_flow()

        if not analysis:
            print("❌ Não há dados para analisar")
            return

        # Identificar ponta
        ponta = self.identify_ponta(analysis)

        # Detectar mudanças
        changes = self.detect_ponta_changes(analysis.get('fluxo_por_barra', []))

        # Construir cenário
        scenario = self.build_flow_scenario(analysis, ponta)

        # Imprimir
        print("\n" + "=" * 100)
        print("🔥 PROFIT PRO — ORDER FLOW ANALYSIS")
        print("=" * 100)

        print(scenario)

        if changes:
            print("\n🚨 MUDANÇAS DETECTADAS:")
            print("-" * 100)
            for change in changes[-10:]:  # Últimas 10 mudanças
                print(f"⏰ {change['timestamp']}")
                print(f"   {change['tipo']}: {change['descricao']}")
                print(f"   ➜ Sinal: {change['sinal']}")
                print()

        print("=" * 100)
        print("✅ ANÁLISE CONCLUÍDA")
        print("=" * 100)

        # Salvar JSON
        output_file = os.path.join(
            os.path.dirname(self.csv_file),
            'profit_flow_analysis.json'
        )

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'analysis': analysis,
                'ponta': ponta,
                'changes': changes,
            }, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Análise salva em: {output_file}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE = os.path.join(BASE_DIR, 'output', 'profit_export.csv')

    # Verificar se arquivo existe
    if not os.path.exists(CSV_FILE):
        print(f"⚠️ Arquivo não encontrado: {CSV_FILE}")
        print("\nPara usar este script:")
        print("1. Exporte dados do Profit Pro:")
        print("   Ferramentas → Exportar Dados")
        print("2. Salve como: output/profit_export.csv")
        print("3. Rode novamente este script")
    else:
        analyzer = ProfitFlowAnalyzer(CSV_FILE)
        analyzer.print_report()
