import pandas as pd
import numpy as np
import random


# putanja_fajla = '/Users/4c/Desktop/GHQ/data/loto7_4708_k85.csv'
# putanja_fajla = '/Users/4c/Desktop/GHQ/data/loto7_4708_k85_loto_2976.csv'
putanja_fajla = '/Users/4c/Desktop/GHQ/data/loto7_4708_k85_loto_plus_1732.csv'


MAX_BROJ = 39
BROJ_KUGLICA = 7

# Postavljanje seed-a za ponovljivost rezultata
random.seed(39)
np.random.seed(39)

# 1. UCITAVANJE BEZ HEADER-A
df = pd.read_csv(putanja_fajla, header=None)

# Uzimam tacno poslednjih 7 kolona iz svakog reda
# Pošto je fajl hronološki, zadnji red (na repu) je najnovije izvlačenje
istorija_izvlacenja = df.iloc[:, -BROJ_KUGLICA:].values.tolist()

# 2. MARKOVLJEVA MATRICA PRELAZA
matrica_prelaza = np.zeros((MAX_BROJ + 1, MAX_BROJ + 1))

for kolo in istorija_izvlacenja:
    kolo_ocisceno = [int(x) for x in kolo if pd.notna(x)]
    if len(kolo_ocisceno) == BROJ_KUGLICA:
        sortirano_kolo = sorted(kolo_ocisceno)
        for i in range(len(sortirano_kolo) - 1):
            trenutni = sortirano_kolo[i]
            sledeci = sortirano_kolo[i+1]
            if 1 <= trenutni <= MAX_BROJ and 1 <= sledeci <= MAX_BROJ:
                matrica_prelaza[trenutni][sledeci] += 1

# Normalizacija u verovatnoće
for i in range(1, MAX_BROJ + 1):
    suma = np.sum(matrica_prelaza[i])
    if suma > 0:
        matrica_prelaza[i] = matrica_prelaza[i] / suma
    else:
        matrica_prelaza[i][1:] = 1.0 / MAX_BROJ

# 3. GENERISANJE TIKETA
def generisi_markov_tiket(pocetni_broj, matrica, duzina_tiketa, max_broj):
    # Osiguravam da je početni broj čist int (uzimam prvi ako je slučajno lista/niz)
    if isinstance(pocetni_broj, (list, np.ndarray)):
        trenutni = int(pocetni_broj[0])
    else:
        trenutni = int(pocetni_broj)
        
    tiket = [trenutni]
    svi_brojevi = list(range(1, max_broj + 1))
    
    while len(tiket) < duzina_tiketa:
        # Uzimam red iz matrice, pretvaram ga u ravan 1D niz i osiguravam tipove
        verovatnoce = np.asarray(matrica[int(trenutni)][1:]).flatten()
        
        # Izbor sledećeg broja - uzimam nulti element jer choices vraća listu
        izabrani = int(random.choices(svi_brojevi, weights=verovatnoce)[0])
        
        if izabrani not in tiket:
            tiket.append(izabrani)
            trenutni = izabrani
        else:
            # Ako je duplikat, biram nasumičan broj koji već NIJE u tiketu
            slobodni_brojevi = [b for b in svi_brojevi if b not in tiket]
            if slobodni_brojevi:
                trenutni = int(random.choice(slobodni_brojevi))
            else:
                break
                
    return sorted(tiket)



# Uzimam poslednji red iz istorije (najnovije kolo)
poslednje_kolo = [int(x) for x in istorija_izvlacenja[-1] if pd.notna(x)]

# Uzimamo najmanji broj iz tog kola kao start, i eksplicitno ga pretvaramo u int
if poslednje_kolo:
    pocetni_broj = int(sorted(poslednje_kolo)[0])
else:
    pocetni_broj = random.randint(1, MAX_BROJ)

# Pokretanje generisanja
novi_tiket = generisi_markov_tiket(pocetni_broj, matrica_prelaza, BROJ_KUGLICA, MAX_BROJ)

print()
print(f"Predloženi tiket: {novi_tiket}")
print()
"""
Predloženi tiket: [10, 12, 15, 17, 21, 26, 32]



Predloženi tiket: [1, 3, 6, 8, 12, 17, 23]



Predloženi tiket: [10, 12, 15, 17, 20, 25, 31]
"""


# Russian mathematician Andrei Markov
