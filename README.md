# IF3170 - G10 Berani dan Tampan

## Deskripsi
Repository ini berisi implementasi tugas besar Inteligensi Artifisial IF3170.

Persoalan yang diangkat dalam tugas besar ini adalah optimasi penempatan paket ke dalam peti kemas pada sebuah truk. Setiap paket memiliki karakteristik yang berbeda, meliputi dimensi (panjang, lebar, dan tinggi), nilai barang (value), berat (weight), status barang pecah-belah (isFragile), serta estimasi waktu kedatangan (Estimated Time of Arrival atau ETA). Sementara itu, peti kemas memiliki dimensi ruang dan kapasitas angkut maksimum yang terbatas. Dengan keterbatasan tersebut, tidak semua paket harus dimasukkan ke dalam peti kemas.

Tujuan utama dari persoalan ini adalah menentukan konfigurasi penempatan paket yang dapat memaksimalkan total nilai barang yang diangkut oleh truk. Konfigurasi tersebut mencakup pemilihan paket yang akan dimuat, penentuan posisi setiap paket dalam ruang tiga dimensi, serta orientasi paket. Setiap paket berbentuk kubus atau balok dan dapat memiliki hingga enam kemungkinan orientasi berdasarkan rotasi terhadap sumbu koordinat. Seluruh posisi paket direpresentasikan menggunakan koordinat bilangan bulat.

Algoritma pencarian yang tersedia:

- Simulated Annealing
- Genetic Algorithm
- Hill Climbing

## Struktur Repository

```text
.
├── src/
│   ├── main.py                 # Entry point program utama
│   ├── app/                    # Menyusun flow utama untuk program
│   ├── localsearch/            # Implementasi algoritma pencarian
│   ├── model/                  # Model yang digunakan dalam menyelesaikan persoalan
│   ├── reader/                 # Membaca input
│   ├── type/                   # Tipe data sederhana
│   ├── visualizer/             # Visualisasi hasil
│   └── open_visualizer.py      # Membuka hasil visualisasi tersimpan (dari folder output)
├── tests/                      # File input JSON untuk pengujian
├── output/                     # File hasil visualisasi
└── README.md
```

## Setup
Clone repository ini:

```bash
git clone https://github.com/NikSamSim/IF3170_G10_BeraniDanTampan
cd IF3170_G10_BeraniDanTampan
```
Gunakan Python 3.10 atau versi yang lebih baru.

Install dependency menggunakan pip:

```bash
pip install matplotlib numpy
```

Jalankan perintah dari root repository:

## Menjalankan Program

Format umum:

```bash
python src/main.py <algorithm_type> <input_filename> <output_filename> [options]
```

`input_filename` harus merupakan file JSON yang berada di folder `tests`.
`output_filename` adalah nama file visualisasi yang akan disimpan di folder
`output`.
`[options]` berarti sejumlah parameter tambahan yang spesifik untuk masing-masing algoritma

## Parameter Opsional

Parameter ditulis dengan format `--nama_parameter nilai`. Parameter yang tidak
diberikan akan menggunakan nilai default dari implementasi algoritma, kecuali
parameter yang ditandai **wajib**.

### Simulated Annealing

| Parameter | Tipe | Contoh | Keterangan |
|---|---|---:|---|
| `--temperature` | `float` | `100` | Suhu awal pencarian. |
| `--min_temperature` | `float` | `0.1` | Suhu minimum sebelum proses berhenti. |
| `--alpha` | `float` | `0.95` | Faktor pendinginan pada setiap iterasi. |
| `--max_iteration` | `int` | `100` | Jumlah maksimum iterasi. |


```bash
python src/main.py simulated_annealing dummy-data-example.json sa.pickle --temperature 100 --alpha 0.95 --min_temperature 0.1 --max_iteration 100
```

### Genetic Algorithm

| Parameter | Tipe | Contoh | Keterangan |
|---|---|---:|---|
| `--population_size` | `int` | `20` | Jumlah individu dalam population; minimal `2`. |
| `--max_iterations` | `int` | `100` | Jumlah maksimum iterasi; minimal `0`. |
| `--seed` | `int` | `None` | Seed random agar hasil dapat direproduksi. |

```bash
python src/main.py genetic_algorithm dummy-data-example.json ga.pickle --population_size 20 --max_iterations 100 --seed 42
```

### Steepest Ascent Hill Climbing

```bash
python src/main.py steepest dummy-data-example.json steepest.pickle 
```

### Stochastic Ascent Hill Climbing

```bash
python src/main.py stochastic dummy-data-example.json stochastic.pickle 
```

### Random Restart Hill Climbing

| Parameter | Tipe | Contoh | Keterangan |
|---|---|---:|---|
| `--max_restart` | `int` | `20` | Banyak restart maksimum, minimal 0 |

```bash
python src/main.py random_restart dummy-data-example.json random_restart.pickle --max_restart 3
```

### Sideways Hill Climbing

| Parameter | Tipe | Contoh | Keterangan |
|---|---|---:|---|
| `--max_side_move` | `int` | `20` | Banyak pergerakan ke samping (flat) maksimum, minimal 0 |

```bash
python src/main.py sideways dummy-data-example.json sideways.pickle --max_side_move 3
```

## Membuka Hasil Visualisasi

Setelah program selesai, file hasil berada di folder `output`. Untuk membuka
hasil visualisasi:

```bash
python src/open_visualizer.py sa.pickle
```

## Format Input

Contoh minimal file input:

```json
{
  "trucks": [
    {
      "dimension": { "w": 10, "l": 20, "h": 5 },
      "maxCapacity": 500
    }
  ],
  "packages": [
    {
      "id": "Package-1",
      "dimension": { "w": 3, "l": 4, "h": 1 },
      "orientation": { "w": "x", "l": "y", "h": "z" },
      "value": 60,
      "weight": 5,
      "isFragile": false,
      "ETA": 3
    }
  ]
}
```

## Pembagian Tugas

| NIM | Anggota | Tugas |
|--- | ---|---|
| 13524029 | Niko Samuel Simanjuntak | Genetic Algorithm, Visualizer, Laporan |
| 13524030 | Irvin Tandiarrang Sumual | Simulated Annealing, Visualizer, Laporan |
| 13524033 | Ray Owen Martin | Hill Climbing, Visualizer, Laporan |
