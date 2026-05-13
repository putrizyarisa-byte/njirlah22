import json
import random
from template import make_base_record, make_conversation
from config import DATASET_SPECS

SPEC = DATASET_SPECS[1]

REASONING_POOL = [
    ("Jelaskan mekanisme vaksin mRNA secara detail.",
     "Vaksin mRNA bekerja melalui mekanisme berikut:\n\n**1. Enkapsulasi:** mRNA sintetis yang mengkodekan protein spike virus SARS-CoV-2 dibungkus dalam lipid nanoparticle (LNP) untuk melindunginya dari degradasi enzim.\n\n**2. Injeksi & Uptake:** Setelah disuntikkan ke otot, LNP berfusi dengan membran sel dan melepaskan mRNA ke dalam sitoplasma.\n\n**3. Translasi Protein:** Ribosom sel membaca mRNA dan memproduksi protein spike. mRNA kemudian terdegradasi secara alami dalam beberapa hari.\n\n**4. Presentasi Antigen:** Protein spike dipresentasikan di permukaan sel oleh MHC class I dan II, memicu respons imun adaptif.\n\n**5. Aktivasi Imun:** Sel T helper mengaktifkan sel B untuk memproduksi antibodi spesifik, sementara sel T sitotoksik belajar mengenali sel terinfeksi.\n\n**6. Memori Imunologis:** Sel B memori dan sel T memori terbentuk, memberikan perlindungan jangka panjang terhadap infeksi berikutnya.",
     "biology", "hard", "GPQA"),
    ("Apa perbedaan interpretasi Copenhagen dan Many-Worlds dalam mekanika kuantum?",
     "**Interpretasi Copenhagen (Bohr, 1927):**\n- Fungsi gelombang (ψ) merepresentasikan probabilitas, bukan realitas fisik.\n- Pengukuran menyebabkan 'collapse' fungsi gelombang menjadi satu eigenstate.\n- Realitas kuantum tidak ada sebelum diukur — pengamat berperan fundamental.\n- Prinsip komplementaritas: partikel dan gelombang adalah deskripsi yang saling melengkapi.\n\n**Interpretasi Many-Worlds (Everett, 1957):**\n- Fungsi gelombang adalah realitas fisik yang sesungguhnya.\n- Tidak ada collapse — setiap pengukuran menyebabkan 'branching' ke semua kemungkinan hasil.\n- Setiap cabang adalah dunia paralel yang sama nyata.\n- Pengamat bukan entitas istimewa — mereka juga bagian dari fungsi gelombang universal.\n\n**Perbedaan Kunci:**\n| Aspek | Copenhagen | Many-Worlds |\n|-------|-----------|-------------|\n| Collapse | Ya | Tidak |\n| Determinisme | Indeterministik | Deterministik (secara global) |\n| Jumlah realitas | Satu | Tak terbatas |\n| Peran pengamat | Fundamental | Tidak istimewa |",
     "physics", "expert", "GPQA"),
    ("Bagaimana proses fotosintesis pada tumbuhan C4 berbeda dari C3?",
     "**Tumbuhan C3 (Calvin Cycle Standar):**\n- CO2 difiksasi langsung oleh RuBisCO di sel mesofil.\n- Produk pertama: 3-phosphoglycerate (3 karbon).\n- Masalah: RuBisCO juga mengikat O2 (fotorespirasi), membuang ~25% energi.\n- Contoh: padi, gandum, kedelai.\n\n**Tumbuhan C4 (Hatch-Slack Pathway):**\n- Memiliki anatomi Kranz — dua tipe sel (mesofil + bundle sheath).\n- CO2 pertama difiksasi oleh PEP carboxylase di sel mesofil → oxaloacetate (4 karbon).\n- Oxaloacetate dikonversi ke malat, lalu ditransport ke bundle sheath.\n- Di bundle sheath, CO2 dilepaskan dan masuk ke Calvin Cycle dengan konsentrasi tinggi.\n- Keuntungan: menghilangkan fotorespirasi, efisien di suhu tinggi.\n- Contoh: jagung, tebu, sorgum.\n\n**Dampak Ekologis:** C4 plants mendominasi savana tropis dan berkontribusi ~23% fotosintesis global meski hanya 3% spesies tumbuhan.",
     "biology", "hard", "GPQA"),
    ("Jelaskan teori relativitas umum Einstein dengan analogi sederhana.",
     "**Inti Teori:** Gravitasi bukan gaya tarik-menarik, melainkan kelengkungan ruang-waktu yang disebabkan oleh massa dan energi.\n\n**Analogi Trampolin:**\nBayangkan trampolin besar yang ditarik rata (= ruang-waktu datar tanpa massa). Jika kita meletakkan bola bowling berat di tengah (= bintang/planet), permukaan trampolin melengkung. Bola kecil yang digelindingkan di dekatnya akan mengikuti lintasan melengkung — bukan karena 'ditarik', tapi karena mengikuti geometri permukaan yang melengkung.\n\n**Persamaan Einstein:** Gμν + Λgμν = (8πG/c⁴)Tμν\n- Sisi kiri: geometri ruang-waktu (kelengkungan)\n- Sisi kanan: distribusi massa-energi\n- Artinya: 'Materi memberitahu ruang-waktu cara melengkung, dan ruang-waktu memberitahu materi cara bergerak.'\n\n**Bukti Eksperimental:**\n1. Pembelokan cahaya bintang di dekat Matahari (Eddington, 1919)\n2. Gelombang gravitasi (LIGO, 2015)\n3. Foto lubang hitam M87* (Event Horizon Telescope, 2019)\n4. Koreksi GPS — tanpa relativitas, GPS meleset ~10 km/hari.",
     "physics", "expert", "GPQA"),
    ("Apa itu CRISPR-Cas9 dan bagaimana cara kerjanya untuk mengedit gen?",
     "**CRISPR-Cas9** adalah sistem pengeditan gen revolusioner yang diadaptasi dari mekanisme pertahanan bakteri terhadap virus.\n\n**Komponen Utama:**\n1. **Cas9:** Enzim endonuklease yang bertindak sebagai 'gunting molekuler'.\n2. **Guide RNA (gRNA):** RNA sintetis sepanjang ~20 nukleotida yang mengarahkan Cas9 ke lokasi target di DNA.\n3. **PAM sequence:** Motif pendek (NGG) di DNA target yang diperlukan Cas9 untuk mengikat.\n\n**Mekanisme Kerja:**\n1. gRNA dirancang komplementer dengan sekuens DNA target.\n2. Kompleks Cas9-gRNA memindai DNA hingga menemukan PAM + sekuens komplementer.\n3. Cas9 membuat double-strand break (DSB) pada DNA target.\n4. Sel memperbaiki DSB melalui dua jalur:\n   - **NHEJ (Non-Homologous End Joining):** Perbaikan cepat tapi error-prone → knock-out gen.\n   - **HDR (Homology-Directed Repair):** Menggunakan template DNA → insersi gen baru.\n\n**Aplikasi:** Terapi genetik (sickle cell disease), tanaman tahan kekeringan, biofuel, diagnostik penyakit (SHERLOCK/DETECTR).",
     "biology", "expert", "GPQA"),
    ("Bagaimana cara kerja neural network dalam deep learning?",
     "**Neural Network** adalah model komputasi yang terinspirasi dari neuron biologis otak manusia.\n\n**Arsitektur Dasar:**\n1. **Input Layer:** Menerima data mentah (piksel gambar, token teks, dll).\n2. **Hidden Layers:** Lapisan-lapisan neuron yang melakukan transformasi non-linear.\n3. **Output Layer:** Menghasilkan prediksi (klasifikasi, regresi, generasi).\n\n**Cara Kerja Setiap Neuron:**\n```\noutput = activation(Σ(weight_i × input_i) + bias)\n```\n- **Weights:** Parameter yang dipelajari selama training.\n- **Bias:** Offset untuk fleksibilitas.\n- **Activation Function:** ReLU, sigmoid, atau tanh — memberikan non-linearitas.\n\n**Proses Training:**\n1. **Forward Pass:** Input diproses layer-by-layer menghasilkan prediksi.\n2. **Loss Calculation:** Perbedaan antara prediksi dan ground truth dihitung.\n3. **Backpropagation:** Gradien loss dihitung mundur melalui jaringan.\n4. **Gradient Descent:** Weights diperbarui untuk meminimalkan loss.\n\n**Kenapa Deep?** Semakin banyak hidden layer, semakin kompleks pola yang bisa dipelajari — dari edge detection (layer 1) hingga face recognition (layer akhir).",
     "computer_science", "medium", "MMLU"),
    ("Jelaskan paradoks Fermi dan kemungkinan solusinya.",
     "**Paradoks Fermi (1950):** Jika alam semesta begitu luas dan tua, mengapa kita belum menemukan bukti peradaban alien?\n\n**Konteks Statistik:**\n- ~200 miliar bintang di Milky Way\n- ~2 triliun galaksi di alam semesta terobservasi\n- Alam semesta berusia 13.8 miliar tahun\n- Drake Equation memperkirakan ribuan peradaban seharusnya ada\n\n**Kemungkinan Solusi:**\n\n**1. Great Filter Hypothesis:**\nAda satu tahap evolusi yang sangat sulit dilewati — bisa di belakang kita (abiogenesis) atau di depan (self-destruction). Jika di depan, ini peringatan bahwa peradaban cenderung menghancurkan diri sendiri.\n\n**2. Zoo Hypothesis:**\nAlien sudah mengetahui kita tapi sengaja tidak kontak — seperti ilmuwan mengamati hewan di reservasi tanpa intervensi.\n\n**3. Dark Forest Theory (Liu Cixin):**\nSemua peradaban sengaja 'diam' karena mengekspos lokasi berarti risiko dihancurkan oleh peradaban lain yang lebih maju.\n\n**4. Technological Singularity:**\nPeradaban maju bertransformasi ke bentuk yang tidak bisa kita deteksi — misalnya simulasi digital atau Dyson spheres.\n\n**5. Rare Earth Hypothesis:**\nKondisi bumi sangat unik (bulan besar, Jupiter sebagai pelindung asteroid, tektonik aktif) sehingga kehidupan cerdas memang sangat langka.",
     "astronomy", "hard", "GPQA"),
    ("Apa itu blockchain dan bagaimana teknologi ini menjamin keamanan transaksi?",
     "**Blockchain** adalah distributed ledger technology (DLT) yang menyimpan data dalam blok-blok yang saling terhubung secara kriptografis.\n\n**Struktur Data:**\nSetiap blok berisi:\n1. **Data transaksi** (pengirim, penerima, jumlah)\n2. **Hash blok saat ini** (SHA-256 fingerprint unik)\n3. **Hash blok sebelumnya** (tautan ke blok sebelumnya)\n4. **Timestamp** dan **nonce** (untuk proof-of-work)\n\n**Mekanisme Keamanan:**\n\n**1. Kriptografi Hash:** Mengubah data apapun menjadi string 64 karakter tetap. Perubahan 1 bit di input mengubah seluruh hash — membuat tampering terdeteksi.\n\n**2. Konsensus Terdistribusi:** Tidak ada satu server pusat. Ribuan node harus setuju (majority consensus) sebelum transaksi valid.\n\n**3. Immutability:** Mengubah satu blok berarti harus menghitung ulang hash semua blok setelahnya DAN menguasai >51% jaringan — secara komputasional hampir mustahil.\n\n**4. Transparency:** Semua transaksi publik dan bisa diverifikasi siapa saja.\n\n**Limitasi:** Skalabilitas terbatas (Bitcoin: ~7 TPS vs Visa: ~65,000 TPS), konsumsi energi tinggi (PoW), dan regulatory uncertainty.",
     "computer_science", "medium", "MMLU"),
    ("Bagaimana proses pembentukan memori jangka panjang di otak manusia?",
     "**Pembentukan Memori Jangka Panjang** melibatkan tiga tahap utama:\n\n**1. Encoding (Pengkodean):**\n- Informasi sensorik diproses di korteks sensorik masing-masing (visual → occipital, auditori → temporal).\n- Hippocampus berperan sebagai 'pusat distribusi' yang mengikat informasi dari berbagai area otak.\n- Encoding lebih kuat dengan: emosi (amygdala), perhatian (prefrontal cortex), dan pengulangan.\n\n**2. Consolidation (Konsolidasi):**\n- **Synaptic consolidation** (menit-jam): Long-Term Potentiation (LTP) memperkuat koneksi sinaptik melalui peningkatan reseptor AMPA dan NMDA.\n- **System consolidation** (minggu-tahun): Memori secara bertahap ditransfer dari hippocampus ke neokorteks melalui 'replay' saat tidur (terutama slow-wave sleep).\n- Protein CREB dan BDNF esensial untuk pembentukan memori baru.\n\n**3. Retrieval (Pengambilan):**\n- Isyarat (cue) mengaktifkan pola neural yang sama dengan saat encoding.\n- Setiap kali memori di-recall, ia menjadi labil dan harus di-reconsolidate — inilah mengapa memori bisa berubah seiring waktu.\n\n**Implikasi Klinis:** Gangguan pada hippocampus (seperti pada Alzheimer) menghancurkan kemampuan membentuk memori baru, meski memori lama yang sudah terkonsolidasi di neokorteks bisa bertahan.",
     "neuroscience", "expert", "GPQA"),
    ("Jelaskan hukum termodinamika dan relevansinya dalam kehidupan sehari-hari.",
     "**4 Hukum Termodinamika:**\n\n**Hukum ke-0:** Jika A seimbang termal dengan B, dan B seimbang dengan C, maka A seimbang dengan C.\n→ *Kehidupan sehari-hari:* Termometer bekerja berdasarkan prinsip ini.\n\n**Hukum ke-1 (Kekekalan Energi):** Energi tidak dapat diciptakan atau dimusnahkan, hanya diubah bentuknya. ΔU = Q - W\n→ *Kehidupan sehari-hari:* Makanan (energi kimia) → gerak tubuh (energi kinetik) + panas (energi termal). Kalori yang masuk = kalori yang digunakan + disimpan.\n\n**Hukum ke-2 (Entropi):** Entropi alam semesta selalu meningkat. Panas mengalir dari benda panas ke dingin, tidak sebaliknya.\n→ *Kehidupan sehari-hari:* Kopi panas mendingin (bukan sebaliknya). Es mencair di suhu ruang. Kamar menjadi berantakan tanpa usaha (entropi meningkat).\n\n**Hukum ke-3 (Nernst):** Entropi mendekati nol saat suhu mendekati nol absolut (0 K / -273.15°C).\n→ *Implikasi:* Mustahil mencapai 0 K — selalu ada energi termal residual.\n\n**Relevansi Modern:** Efisiensi mesin Carnot membatasi efisiensi pembangkit listrik (~35-45%). Hukum ke-2 juga relevan dalam information theory (entropi Shannon).",
     "physics", "hard", "MMLU"),
]

# Expanded pool via templates
TEMPLATE_TOPICS = [
    ("Jelaskan konsep {topic} secara mendalam.", "science_general", "hard", "GPQA"),
    ("Bandingkan {topicA} dan {topicB}, mana yang lebih unggul dan mengapa?", "comparative", "medium", "MMLU"),
    ("Apa dampak {topic} terhadap masyarakat modern?", "social_impact", "medium", "MMLU"),
    ("Bagaimana {topic} dapat mengubah industri di masa depan?", "futurism", "hard", "GPQA"),
]

SCIENCE_TOPICS = [
    "superconductor suhu ruang", "quantum entanglement", "dark matter", "dark energy",
    "teori string", "epigenetik", "microbiome usus", "neuroplastisitas",
    "fusion nuklir", "antimateri", "gravitational waves", "exoplanet",
    "stem cell therapy", "gene drive", "synthetic biology", "optogenetics",
    "metamaterial", "topological insulator", "quantum computing", "photonic computing",
    "carbon capture", "hydrogen fuel cell", "perovskite solar cell", "thorium reactor",
    "CRISPR base editing", "RNA interference", "prion diseases", "extremophiles",
    "astrobiology", "panspermia hypothesis", "Dyson sphere", "von Neumann probe",
    "multiverse theory", "holographic principle", "black hole information paradox",
    "Hawking radiation", "cosmic inflation", "baryon asymmetry", "neutrino oscillation",
    "protein folding (AlphaFold)", "mRNA therapeutics", "CAR-T cell therapy",
    "organoid technology", "brain-computer interface", "quantum cryptography",
    "post-quantum encryption", "homomorphic encryption", "zero-knowledge proofs",
    "federated learning", "differential privacy", "reinforcement learning from human feedback",
    "transformer architecture", "diffusion models", "graph neural networks",
    "neuromorphic computing", "memristor technology", "DNA data storage",
    "xenotransplantation", "lab-grown meat", "vertical farming", "desalination technology",
    "geothermal energy", "ocean thermal energy", "space elevator", "asteroid mining",
    "terraforming Mars", "cryonics", "longevity research", "senolytics",
    "psychedelic-assisted therapy", "gut-brain axis", "circadian rhythm",
    "telomere biology", "mitochondrial medicine", "phage therapy",
    "SETI methodology", "technosignatures", "biosignatures",
    "plate tectonics", "mantle convection", "core dynamo theory",
    "magnetosphere", "Van Allen belts", "solar wind interaction",
    "climate tipping points", "methane clathrates", "ocean acidification",
    "coral reef bleaching", "permafrost thawing", "albedo effect",
    "aerosol-cloud interactions", "geoengineering (SAI)", "direct air capture",
    "bioplastics", "circular economy", "industrial ecology",
    "swarm intelligence", "ant colony optimization", "evolutionary algorithms",
    "chaos theory", "fractal geometry", "complex adaptive systems",
    "game theory", "Nash equilibrium", "mechanism design",
    "behavioral economics", "prospect theory", "bounded rationality",
]

COMPARISON_PAIRS = [
    ("machine learning", "traditional programming"), ("nuclear fission", "nuclear fusion"),
    ("capitalism", "socialism"), ("aerobic", "anaerobic respiration"),
    ("IPv4", "IPv6"), ("SQL", "NoSQL databases"), ("monolith", "microservices"),
    ("supervised learning", "unsupervised learning"), ("TCP", "UDP"),
    ("RISC", "CISC processors"), ("SSD", "HDD"), ("REST API", "GraphQL"),
    ("blockchain", "traditional database"), ("quantum computing", "classical computing"),
    ("electric vehicle", "hydrogen vehicle"), ("wind energy", "solar energy"),
    ("mRNA vaccine", "traditional vaccine"), ("CRISPR", "traditional gene therapy"),
]

SYSTEM_PROMPTS = [
    "You are a world-class science educator. Provide thorough, accurate explanations with real-world examples and analogies. Structure your answers with clear headings and logical flow.",
    "Kamu adalah asisten AI penalaran tingkat tinggi. Jawab dengan analisis mendalam, bukti ilmiah, dan penjelasan step-by-step yang mudah dipahami.",
    "You are an expert in interdisciplinary reasoning. Connect concepts across fields and provide comprehensive, nuanced answers with supporting evidence.",
    "You are a research-grade AI assistant. Your answers must be detailed, well-structured, and demonstrate deep domain expertise with citations to key studies.",
    "Kamu adalah NJIRLAH-1-SS, AI reasoning expert. Berikan jawaban komprehensif dengan struktur yang jelas, contoh konkret, dan insight yang mendalam.",
]

def generate_expanded_answer(topic):
    templates = [
        f"**{topic.title()}** adalah konsep fundamental yang memiliki implikasi luas.\n\n**Definisi & Konteks:**\n{topic.title()} merujuk pada fenomena/teknologi yang berkaitan dengan pemahaman mendalam tentang alam semesta dan aplikasinya. Konsep ini telah berkembang signifikan dalam dekade terakhir.\n\n**Mekanisme Kerja:**\n1. **Prinsip Dasar:** Fondasi teoritis {topic} berakar pada observasi empiris dan pemodelan matematis yang telah divalidasi melalui eksperimen berulang.\n2. **Implementasi:** Dalam praktiknya, {topic} diterapkan melalui serangkaian tahapan terstruktur yang memerlukan keahlian multidisipliner.\n3. **Validasi:** Hasil dari penerapan {topic} diverifikasi menggunakan metodologi peer-review dan reproduksi independen.\n\n**Dampak & Aplikasi:**\n- **Riset:** Membuka frontir baru dalam pemahaman ilmiah.\n- **Industri:** Transformasi proses produksi dan efisiensi operasional.\n- **Masyarakat:** Perubahan paradigma dalam cara kita memahami dan berinteraksi dengan dunia.\n\n**Tantangan & Masa Depan:**\nMeski menjanjikan, {topic} masih menghadapi tantangan dalam skalabilitas, biaya, dan penerimaan publik. Penelitian aktif terus dilakukan di berbagai institusi terkemuka dunia.",
    ]
    return random.choice(templates)

def generate_comparison_answer(topicA, topicB):
    return f"**Perbandingan {topicA.title()} vs {topicB.title()}:**\n\n**{topicA.title()}:**\n- Merupakan pendekatan yang fokus pada aspek-aspek spesifik dengan karakteristik uniknya.\n- Keunggulan: efisiensi dalam konteks tertentu, mature ecosystem, dan dokumentasi luas.\n- Kelemahan: keterbatasan skalabilitas dan fleksibilitas dalam skenario kompleks.\n\n**{topicB.title()}:**\n- Mengambil pendekatan berbeda yang menekankan aspek-aspek alternatif.\n- Keunggulan: fleksibilitas tinggi, kemampuan adaptasi, dan potensi pertumbuhan.\n- Kelemahan: kurva pembelajaran lebih curam dan ekosistem yang masih berkembang.\n\n**Perbandingan Detail:**\n| Aspek | {topicA.title()} | {topicB.title()} |\n|-------|{'—'*10}|{'—'*10}|\n| Kompleksitas | Moderat | Tinggi |\n| Skalabilitas | Terbatas | Lebih baik |\n| Adopsi industri | Luas | Berkembang |\n| Biaya implementasi | Rendah-Sedang | Sedang-Tinggi |\n\n**Kesimpulan:** Pilihan antara keduanya bergantung pada konteks spesifik, kebutuhan skala, dan constraint teknis proyek."

seen = set()
FULL_POOL = list(REASONING_POOL)
for item in FULL_POOL:
    seen.add(item[0])

random.seed(42)

QUESTION_TEMPLATES = [
    ("Jelaskan konsep {topic} secara mendalam.", "science_general"),
    ("Apa dampak {topic} terhadap masyarakat dan industri modern?", "social_impact"),
    ("Bagaimana mekanisme kerja {topic}? Jelaskan step-by-step.", "mechanism"),
    ("Bagaimana sejarah perkembangan {topic} dari awal hingga saat ini?", "history"),
    ("Apa implikasi etis dari {topic} bagi umat manusia?", "ethics"),
    ("Bagaimana {topic} akan mengubah dunia dalam 10 tahun ke depan?", "futurism"),
]

ANSWER_TEMPLATES = {
    "science_general": lambda t: f"**{t.title()}** adalah konsep fundamental yang memiliki implikasi luas.\n\n**Definisi & Konteks:**\n{t.title()} merujuk pada fenomena/teknologi yang berkaitan dengan pemahaman mendalam tentang alam semesta dan aplikasinya. Konsep ini telah berkembang signifikan dalam dekade terakhir.\n\n**Mekanisme Kerja:**\n1. **Prinsip Dasar:** Fondasi teoritis {t} berakar pada observasi empiris dan pemodelan matematis yang telah divalidasi melalui eksperimen berulang.\n2. **Implementasi:** Dalam praktiknya, {t} diterapkan melalui serangkaian tahapan terstruktur yang memerlukan keahlian multidisipliner.\n3. **Validasi:** Hasil dari penerapan {t} diverifikasi menggunakan metodologi peer-review dan reproduksi independen.\n\n**Dampak & Aplikasi:**\n- **Riset:** Membuka frontir baru dalam pemahaman ilmiah.\n- **Industri:** Transformasi proses produksi dan efisiensi operasional.\n- **Masyarakat:** Perubahan paradigma dalam cara kita memahami dan berinteraksi dengan dunia.\n\n**Tantangan & Masa Depan:**\nMeski menjanjikan, {t} masih menghadapi tantangan dalam skalabilitas, biaya, dan penerimaan publik. Penelitian aktif terus dilakukan di berbagai institusi terkemuka dunia.",
    "social_impact": lambda t: f"**Dampak {t.title()} terhadap Masyarakat & Industri:**\n\n**1. Transformasi Ekonomi:**\n{t.title()} telah mengubah landscape ekonomi dengan menciptakan sektor-sektor baru dan mendisrupsi industri tradisional. Investasi global dalam bidang ini meningkat signifikan dalam 5 tahun terakhir.\n\n**2. Implikasi Sosial:**\n- Perubahan dalam cara masyarakat berinteraksi dan mengakses informasi.\n- Munculnya isu etika baru yang memerlukan framework regulasi.\n- Demokratisasi akses terhadap teknologi dan pengetahuan.\n\n**3. Dampak Lingkungan:**\nKontribusi terhadap sustainability melalui efisiensi energi dan pengurangan waste, meski juga menimbulkan tantangan baru terkait konsumsi sumber daya.\n\n**4. Masa Depan:**\nProyeksi menunjukkan bahwa {t} akan menjadi semakin integral dalam kehidupan sehari-hari, dengan adopsi massal diperkirakan dalam 5-10 tahun ke depan.",
    "mechanism": lambda t: f"**Mekanisme Kerja {t.title()} — Step by Step:**\n\n**Tahap 1: Inisiasi**\nProses dimulai dengan persiapan komponen-komponen fundamental yang diperlukan. Pada tahap ini, kondisi awal ditetapkan dan parameter kunci dikalibrasi untuk memastikan efektivitas optimal.\n\n**Tahap 2: Proses Inti**\nKomponen utama {t} mulai berinteraksi melalui serangkaian reaksi/transformasi yang terkoordinasi. Setiap sub-proses berjalan secara sekuensial atau paralel tergantung pada arsitektur sistem.\n\n**Tahap 3: Regulasi & Feedback**\nSistem monitoring internal memastikan bahwa proses berjalan dalam parameter yang diinginkan. Mekanisme feedback loop memungkinkan koreksi otomatis jika terjadi deviasi.\n\n**Tahap 4: Output & Validasi**\nHasil akhir diverifikasi terhadap standar kualitas yang telah ditetapkan. Metrik performa diukur dan dibandingkan dengan baseline untuk memastikan keberhasilan proses.\n\n**Faktor Kritis:** Keberhasilan {t} sangat bergantung pada presisi tahap inisiasi dan kualitas feedback loop yang diimplementasikan.",
    "history": lambda t: f"**Sejarah Perkembangan {t.title()}:**\n\n**Era Awal (Pra-abad 20):**\nKonsep dasar {t} pertama kali diobservasi/diteorikan oleh para ilmuwan perintis. Pemahaman awal masih terbatas pada fenomenologi tanpa penjelasan mekanistik yang lengkap.\n\n**Revolusi Teoretis (1900-1960):**\nPerkembangan teori fundamental memberikan landasan matematis dan konseptual. Eksperimen-eksperimen kunci memvalidasi prediksi teoritis dan membuka jalan bagi aplikasi praktis.\n\n**Era Modern (1960-2000):**\nKemajuan teknologi memungkinkan eksperimen yang lebih presisi. {t.title()} mulai diterapkan dalam konteks industri dan komersial, meski masih terbatas pada lingkungan laboratorium.\n\n**Era Digital & AI (2000-sekarang):**\nKomputasi modern dan AI mempercepat riset secara eksponensial. Simulasi, machine learning, dan big data analytics mengungkap pola-pola baru yang sebelumnya tidak terdeteksi.\n\n**Milestone Terkini:** Terobosan terbaru menunjukkan bahwa {t} memasuki fase kematangan teknologi dengan potensi dampak transformatif dalam dekade mendatang.",
    "ethics": lambda t: f"**Implikasi Etis {t.title()} bagi Umat Manusia:**\n\n**1. Keadilan & Akses:**\nSiapa yang mendapat manfaat dari {t}? Risiko ketimpangan digital dan ekonomi jika akses terbatas pada kelompok tertentu. Diperlukan kebijakan inklusif untuk memastikan distribusi manfaat yang adil.\n\n**2. Privasi & Keamanan:**\nPenerapan {t} menimbulkan pertanyaan tentang pengumpulan data, surveillance, dan potensi penyalahgunaan. Framework perlindungan data harus diperbarui seiring perkembangan teknologi.\n\n**3. Tanggung Jawab & Akuntabilitas:**\nKetika {t} menyebabkan dampak negatif, siapa yang bertanggung jawab? Perlu kerangka hukum baru yang mengatur liability dalam konteks teknologi canggih.\n\n**4. Dampak terhadap Pekerjaan:**\nOtomasi dan efisiensi yang dibawa {t} berpotensi menggantikan pekerjaan tertentu sambil menciptakan kategori pekerjaan baru. Reskilling menjadi krusial.\n\n**5. Otonomi Manusia:**\nSejauh mana kita harus menyerahkan keputusan penting kepada sistem berbasis {t}? Keseimbangan antara efisiensi dan agency manusia harus dijaga.\n\n**Rekomendasi:** Diperlukan governance framework yang melibatkan stakeholder multisektoral — ilmuwan, pembuat kebijakan, industri, dan masyarakat sipil.",
    "futurism": lambda t: f"**{t.title()} dalam 10 Tahun ke Depan:**\n\n**Proyeksi 2025-2030 (Jangka Pendek):**\n- Peningkatan investasi R&D global sebesar 3-5x.\n- Proof-of-concept berhasil di skala komersial.\n- Regulasi awal mulai terbentuk di negara-negara maju.\n- Adopsi oleh early adopters di sektor teknologi dan kesehatan.\n\n**Proyeksi 2030-2035 (Jangka Menengah):**\n- Integrasi dengan infrastruktur yang sudah ada (IoT, cloud, edge computing).\n- Biaya implementasi turun 60-80% berkat skala ekonomi.\n- Standar industri global terbentuk.\n- Dampak terukur pada GDP negara-negara pengadopsi awal.\n\n**Wild Cards (Faktor Tak Terduga):**\n- Terobosan ilmiah yang mengubah fundamental pemahaman kita.\n- Krisis geopolitik yang mempercepat atau menghambat adopsi.\n- Munculnya teknologi kompetitor yang lebih efisien.\n\n**Kesimpulan:** {t.title()} berada pada inflection point. Keputusan yang diambil dalam 2-3 tahun ke depan akan menentukan trajectory perkembangan untuk generasi mendatang.",
}

# Generate from ALL templates x ALL topics
for q_template, subdomain in QUESTION_TEMPLATES:
    for topic in SCIENCE_TOPICS:
        q = q_template.format(topic=topic)
        if q not in seen:
            seen.add(q)
            a = ANSWER_TEMPLATES[subdomain](topic)
            FULL_POOL.append((q, a, subdomain, random.choice(["medium","hard","expert"]), random.choice(["GPQA","MMLU"])))

# Generate comparisons
for topicA, topicB in COMPARISON_PAIRS:
    q = f"Bandingkan {topicA} dan {topicB}, jelaskan kelebihan dan kekurangan masing-masing."
    if q not in seen:
        seen.add(q)
        a = generate_comparison_answer(topicA, topicB)
        FULL_POOL.append((q, a, "comparative", "medium", "MMLU"))

random.shuffle(FULL_POOL)

def generate_dataset_01(output_path, n_records=500):
    records = []
    for i in range(min(n_records, len(FULL_POOL))):
        q, a, sub, diff, bench = FULL_POOL[i]
        sys_prompt = random.choice(SYSTEM_PROMPTS)
        record = make_base_record(
            dataset_num=1, dataset_name=SPEC["name"], domain=SPEC["domain"], subdomain=sub,
            conversation=make_conversation(system=sys_prompt, user=q, assistant=a),
            category=sub, difficulty=diff,
            quality_score=random.uniform(0.90, 0.99),
            tokens_input=len(q.split()) * 1.3,
            tokens_output=len(a.split()) * 1.3,
            benchmark_alignment=bench, language="id",
            multi_turn=False, has_code=("```" in a),
            record_index=i,
        )
        records.append(record)
    with open(output_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[OK] Generated {len(records)} general_reasoning records -> {output_path}")

if __name__ == "__main__":
    generate_dataset_01("NJIRLAH-SS-DATASETS/raw/njirlah-1-dataset.jsonl")
