import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import shapiro, pearsonr, spearmanr

class DataAnalyzer:
    def __init__(self, file_name="./data/game_statistics.json"):
        self.file_name = file_name
        self.data = None

    def load_data(self):
        """JSON dosyasından verileri yükler."""
        with open(self.file_name, "r") as file:
            self.data = pd.DataFrame(json.load(file))

    def visualize_data(self):
        """Verilerin zaman içindeki değişimini görselleştirir."""
        plt.figure(figsize=(10, 6))
        for column in self.data.columns:
            if column != "time":  # Zamanı ayrı bir referans olarak kullanıyoruz
                plt.plot(self.data["time"], self.data[column], label=column)
        
        plt.title("Zaman İçindeki İstatistikler")
        plt.xlabel("Zaman (saniye)")
        plt.ylabel("Değer")
        plt.legend()
        plt.grid()
        plt.show()

    def correlation_analysis(self):
        """Korelasyon matrisini hesaplar ve görselleştirir."""
        corr_matrix = self.data.corr()
        print("Korelasyon Matrisi:")
        print(corr_matrix)

        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title("Korelasyon Matrisi")
        plt.show()

    def distribution_analysis(self):
        """Her bir değişkenin normal dağılıma uygunluk testini yapar."""
        results = {}
        for column in self.data.columns:
            if column != "time":  # Zamanı analiz etmiyoruz
                stat, p_value = shapiro(self.data[column])
                results[column] = {"statistic": stat, "p_value": p_value}
        
        print("\nNormal Dağılıma Uygunluk Testi Sonuçları:")
        for column, result in results.items():
            print(f"{column}: Statistic={result['statistic']:.4f}, p-value={result['p_value']:.4f}")
            if result["p_value"] > 0.05:
                print(f"    {column} normal dağılıma uygundur.")
            else:
                print(f"    {column} normal dağılıma uygun değildir.")

    def run_all(self):
        """Tüm analizleri çalıştırır."""
        print("Veriler Yükleniyor...")
        self.load_data()
        
        print("\nVeriler Görselleştiriliyor...")
        self.visualize_data()

        print("\nKorelasyon Analizi Yapılıyor...")
        self.correlation_analysis()

        print("\nDağılım Analizi Yapılıyor...")
        self.distribution_analysis()


if __name__ == "__main__":
    analyzer = DataAnalyzer()
    analyzer.run_all()
