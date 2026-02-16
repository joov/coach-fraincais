# Coach Français – Anforderungsbeschreibung

## Überblick

Der **Coach Français** ist ein interaktiver KI-gestützter Französisch-Coach. Er kommuniziert hauptsächlich auf Französisch mit dem Nutzer und bietet drei Kernfunktionen: Trainingsplan erstellen, Interaktiv üben und Erfolge kontrollieren.

Das didaktische Konzept orientiert sich an bewährten FLE-Lehrbüchern (Français Langue Étrangère): Jede Lektion behandelt eine **konkrete Alltagssituation** und folgt einem festen Ablauf – vom Hören und Nachsprechen eines Dialogs über gezielte Übungen bis zur freien Anwendung. Die Lektionen bauen aufeinander auf und bilden einen **kontinuierlichen Lernpfad** vom Anfänger- bis zum Fortgeschrittenenniveau.

---

## Grundprinzipien

- **Sprache:** Der Coach kommuniziert so weit wie möglich auf Französisch. Grammatikerklärungen und Hinweise dürfen bei niedrigem Niveau (A1-A2) auf Deutsch gegeben werden. Ab Niveau B1 wird konsequent Französisch verwendet.
- **Ton:** Sachlich-neutral. Fokus auf Inhalt, Korrektheit und Effizienz. Kein überflüssiger Smalltalk, aber höflich und respektvoll.
- **Niveau:** Der Nutzer wählt beim Start sein aktuelles Sprachniveau (A1–C2). Der Coach passt Schwierigkeitsgrad, Vokabular und Komplexität der Übungen entsprechend an.
- **Gedächtnis:** Der Coach merkt sich den Namen des Nutzers, das gewählte Niveau und bisherige Fortschritte über Sessions hinweg. So kann er an frühere Übungen anknüpfen und die Lernkurve nachvollziehen.

---

## Funktion 1: Trainingsplan erstellen

### Beschreibung

Der Trainingsplan ist eine **geordnete Liste von Lektionen**, die jeweils eine typische Gesprächssituation behandeln. Die Lektionen sind so angeordnet, dass ein kontinuierlicher Fortschritt der Sprachfähigkeit erreicht wird – von einfachen Begrüßungen bis hin zu komplexen Alltagssituationen.

Der Coach erstellt den Trainingsplan **individuell** auf Basis von vier Eingaben des Nutzers:

### Eingaben zur Planerstellung

#### 1. Zielniveau (Pflicht)
Der Nutzer gibt an, welches Sprachniveau er erreichen möchte (A1, A2, B1, B2, C1, C2). Der Coach wählt daraufhin die passenden Lektionen und Grammatik-Inhalte aus, die für das Erreichen dieses Ziels nötig sind. Liegt das aktuelle Niveau des Nutzers z.B. bei A1 und das Ziel bei A2, werden nur die Lektionen eingeplant, die den Übergang von A1 nach A2 abdecken.

#### 2. Grammatik-Schwerpunkte (Optional)
Der Nutzer kann gezielt Grammatikthemen benennen, die er besonders üben möchte (z.B. „Passé composé", „Subjonctif", „Artikel und Genus", „Verneinung"). Der Coach gewichtet diese Themen im Plan höher – die betreffenden Lektionen werden priorisiert und ggf. mit zusätzlichen Vertiefungsübungen ergänzt.

**Beispiel:**
```
Nutzer: Ich möchte besonders den Passé composé üben.
Coach:  D'accord. Die Lektionen mit Fokus auf Passé composé werden
        priorisiert und um zusätzliche Konjugations- und
        Lückentextübungen ergänzt.
```

#### 3. Themenvorgaben (Optional)
Der Nutzer kann Alltagsthemen benennen, die für ihn besonders relevant sind (z.B. „Restaurant", „Arztbesuch", „Einkaufen", „Reisen"). Der Coach verschiebt die entsprechenden Lektionen weiter nach vorne im Plan und baut bei Bedarf zusätzliche situationsbezogene Dialoge ein.

**Beispiel:**
```
Nutzer: Ich reise bald nach Paris und brauche vor allem
        Restaurant, Hotel und Wegbeschreibung.
Coach:  Compris. Ich priorisiere die Blöcke „Unterwegs in der Stadt",
        „Einkaufen und Essen" und „Reisen". Die anderen Themen
        werden danach eingeplant.
```

#### 4. Zeitbudget (Pflicht)
Der Nutzer gibt an, wie viel Zeit er pro Tag und pro Woche aufwenden möchte. Basierend darauf verteilt der Coach die Lektionen über die verfügbare Zeit. Jede Lektion dauert ca. 15–30 Minuten.

### Plangenerierung

Der Coach kombiniert die vier Eingaben zu einem individuellen Plan:
1. Aus dem **Zielniveau** ergibt sich, welche Lektionen und Grammatik-Inhalte nötig sind.
2. Durch **Grammatik-Schwerpunkte** werden bestimmte Lektionen priorisiert und vertieft.
3. Durch **Themenvorgaben** wird die Reihenfolge der Blöcke angepasst.
4. Das **Zeitbudget** bestimmt die Verteilung über Tage und Wochen.

Der resultierende Plan bleibt jederzeit anpassbar – der Nutzer kann Schwerpunkte ändern, Themen ergänzen oder das Zeitbudget korrigieren.

### Lektionsübersicht (Beispiel für Niveau A1–A2)

Der Trainingsplan orientiert sich an alltagsrelevanten Situationen, gegliedert in thematische Blöcke mit steigendem Schwierigkeitsgrad:

**Block 1 – Erste Kontakte (Lektionen 1–9)**
| Nr. | Thema | Grammatik-Schwerpunkt |
|-----|-------|----------------------|
| 1 | Saluer (Grüßen) | – |
| 2 | Dire bonjour (Guten Tag sagen) | Formell vs. informell (tu/vous) |
| 3 | Dire au revoir (Verabschieden) | Wochentage, Zeitangaben |
| 4 | L'état civil et la nationalité | Le verbe ÊTRE |
| 5 | L'alphabet | Buchstabieren |
| 6 | La famille | Compter de 0 à 20; Le verbe AVOIR |
| 7 | Se présenter (Sich vorstellen) | Le verbe S'APPELER |
| 8 | J'habite… (Wo ich wohne) | Le verbe HABITER |
| 9 | Adresse et numéro de téléphone | Compter jusqu'à 99 |
| -- | **Bilan (Zwischentest)** | Wiederholung Block 1 |

**Block 2 – Zeit, Wetter und Beruf (Lektionen 10–15)**
| Nr. | Thema | Grammatik-Schwerpunkt |
|-----|-------|----------------------|
| 10 | Demander / dire l'heure | Uhrzeiten |
| 11 | La date | Monate und Jahreszeiten |
| 12 | Le temps qu'il fait | Wetter-Ausdrücke |
| 13 | S'excuser | Höflichkeitsformen |
| 14 | Les professions (1) | Le verbe FAIRE |
| 15 | Les professions (2) | Le verbe TRAVAILLER |

**Block 3 – Unterwegs in der Stadt (Lektionen 16–26)**
| Nr. | Thema | Grammatik-Schwerpunkt |
|-----|-------|----------------------|
| 16 | Où allez-vous ? (1) | Le verbe ALLER |
| 17 | Où allez-vous ? (2) | Ortsangaben |
| 18 | D'où venez-vous ? (1) | Le verbe VENIR |
| 19 | D'où venez-vous ? (2) | Herkunft und Ländernamen |
| 20 | Les transports (1) | Le verbe PARTIR |
| 21 | Les transports (2) | Le verbe ARRIVER |
| 22 | Les transports (3) | Le verbe PRENDRE |
| 23 | Se situer dans l'espace | Le verbe SAVOIR |
| 24 | La ville | Stadtvokabular |
| 25 | Demander son chemin (1) | Le verbe CHERCHER |
| 26 | Demander son chemin (2) | Bus und Métro |

**Block 4 – Einkaufen und Essen (Lektionen 27–39)**
| Nr. | Thema | Grammatik-Schwerpunkt |
|-----|-------|----------------------|
| 27 | À la boulangerie | Le verbe ACHETER |
| 28 | À la pâtisserie | Mengenangaben |
| 29 | Dans un café : les boissons | Bestellen |
| 30 | Au marché : les légumes | Gemüsevokabular |
| 31 | Au marché : les fruits | Obstvokabular |
| 32 | L'alimentation générale : à l'épicerie | Lebensmittelvokabular |
| 33 | Boucherie-charcuterie et poissonnerie | Fleisch und Fisch |
| 34 | Les différents repas | Mahlzeiten und Verben |
| 35 | L'alimentation | Les verbes MANGER et VOULOIR |
| 36 | L'alimentation | Le verbe BOIRE |
| 37 | Au restaurant | Restaurantbesuch |
| 38 | Au restaurant : cas particuliers | Probleme und Beschwerden |
| 39 | Goûts et préférences | Les verbes AIMER, ADORER, DÉTESTER |

**Block 5 – Gesundheit und Behörden (Lektionen 40–46)**
| Nr. | Thema | Grammatik-Schwerpunkt |
|-----|-------|----------------------|
| 40 | Prendre rendez-vous chez le médecin | Terminvereinbarung |
| 41 | Chez le médecin (1) | Le corps humain; AVOIR MAL |
| 42 | Chez le médecin (2) | Les symptômes |
| 43 | Chez le médecin (3) | Les accidents ménagers |
| 44 | À la pharmacie | Medikamente |
| 45 | À la poste | Postvokabular |
| 46 | À la préfecture | Behördengang |

**Block 6 – Einkaufen und Freizeit (Lektionen 47–55)**
| Nr. | Thema | Grammatik-Schwerpunkt |
|-----|-------|----------------------|
| 47 | Dans un magasin de vêtements (1) | Kleidung |
| 48 | Dans un magasin de vêtements (2) | Farben, Größen |
| 49 | Dans un magasin de chaussures | Schuhe |
| 50 | Chez le coiffeur | Beim Friseur |
| 51 | Au club de sport | Sport-Anmeldung |
| 52 | Les sports | Sportarten |
| 53 | À la banque | Bankgeschäfte |
| 54 | Au bureau | Im Büro |
| 55 | Arriver à un rendez-vous | Termine wahrnehmen |

**Block 7 – Reisen und Notfälle (Lektionen 56–65)**
| Nr. | Thema | Grammatik-Schwerpunkt |
|-----|-------|----------------------|
| 56 | À l'hôtel : Réserver une chambre | Reservierung |
| 57 | À l'hôtel : Critique et réclamation | Beschwerde |
| 58 | Le système scolaire français | Schulsystem |
| 59 | Les fêtes et les célébrations | Le verbe OFFRIR |
| 60 | Au commissariat (1) | Diebstahl melden |
| 61 | Au commissariat (2) | Einbruch melden |
| 62 | En cas d'incendie : Appeler le 112 | Notruf (Feuer) |
| 63 | En cas d'accident : Appeler le 112 | Notruf (Unfall) |
| 64 | Louer une voiture | Mietwagen |
| 65 | La voiture | Auto-Vokabular |

### Ergänzend: 30 wichtige Verben im Präsens

Begleitend zu den Lektionen wird die Konjugation der 30 wichtigsten Alltagsverben systematisch geübt:
ÊTRE, AVOIR, S'APPELER, PARLER, HABITER, TRAVAILLER, ARRIVER, CHERCHER, DÉJEUNER, DÎNER, AIMER, ADORER, PRÉFÉRER, DÉTESTER, JOUER, MANGER, VOYAGER, ACHETER, ALLER, FAIRE, VENDRE, VENIR, PARTIR, PRENDRE, APPRENDRE, COMPRENDRE, SAVOIR, DESCENDRE, VOULOIR, BOIRE.

### Zeitplanung

Der Coach verteilt die Lektionen entsprechend dem Zeitbudget des Nutzers. Die Gesamtdauer hängt vom Zielniveau und der Anzahl benötigter Lektionen ab:

| Beispiel | Übungszeit | Lektionen/Woche | Dauer (alle 65 Lektionen) | Dauer (20 Lektionen, z.B. A1→A2) |
|----------|-----------|-----------------|---------------------------|----------------------------------|
| Intensiv | 30 Min/Tag, 5 Tage/Woche | 5 | ca. 13 Wochen | ca. 4 Wochen |
| Moderat | 20 Min/Tag, 3 Tage/Woche | 3 | ca. 22 Wochen | ca. 7 Wochen |
| Entspannt | 15 Min/Tag, 2 Tage/Woche | 2 | ca. 33 Wochen | ca. 10 Wochen |

### Beispiel eines generierten Trainingsplans

```
Eingaben:
  Aktuelles Niveau: A1
  Zielniveau:        A2
  Schwerpunkt:       Passé composé, Verben der Bewegung
  Themen:            Restaurant, Wegbeschreibung, Einkaufen
  Zeitbudget:        20 Min/Tag, 3 Tage/Woche

Generierter Plan (Auszug):
  Woche 1:  Lektion 1 – Saluer
            Lektion 2 – Dire bonjour
            Lektion 3 – Dire au revoir
  Woche 2:  Lektion 25 – Demander son chemin (1) ⭐ Themen-Priorität
            Lektion 26 – Demander son chemin (2) ⭐ Themen-Priorität
            Lektion 4 – L'état civil et la nationalité
  Woche 3:  Lektion 37 – Au restaurant ⭐ Themen-Priorität
            Lektion 38 – Au restaurant : cas particuliers ⭐ Themen-Priorität
            Lektion 27 – À la boulangerie ⭐ Themen-Priorität
  ...
  Woche 5:  Vertiefung Passé composé ⭐ Grammatik-Schwerpunkt
            (zusätzliche Konjugations- und Lückentextübungen)
  ...
```

---

## Funktion 2: Interaktiv üben

### Beschreibung

Jede Lektion folgt einem **festen dreistufigen Ablauf**, der sich am bewährten Muster von FLE-Lehrbüchern orientiert:

1. **Schritt 1: Dialog hören und nachsprechen** (Écoutez et répétez)
2. **Schritt 2: Schriftliche Übungen** (Pratiquez)
3. **Schritt 3: Grammatik-Zusammenfassung** (Grammatik-Box)

### Grundprinzip: Jede Übung in zwei Formen – formell und informell

Jede Lektion wird grundsätzlich in **zwei Varianten** durchgeführt: einer **formellen** und einer **informellen** Fassung. Das betrifft sowohl die Dialoge (Schritt 1) als auch die schriftlichen Übungen (Schritt 2).

- **Informell (tu):** Gespräch unter Freunden, Bekannten, Gleichaltrigen. Lockerer Ton, Umgangssprache erlaubt.
- **Formell (vous):** Gespräch mit Unbekannten, im beruflichen Kontext, mit Respektspersonen. Höflicher Ton, vollständige Sätze.

Der Nutzer übt dadurch **dieselbe Alltagssituation in beiden Registern** und lernt, sicher zwischen den Sprachebenen zu wechseln. Die formelle und informelle Variante sind jeweils eigene Teilübungen innerhalb der Lektion.

**Warum beides?** Im Französischen ist die Unterscheidung tu/vous fundamental und durchzieht Vokabular, Konjugation, Pronomen und Redewendungen. Wer nur eine Form beherrscht, kann in realen Situationen schnell in Schwierigkeiten geraten.

### Schritt 1: Dialog hören und nachsprechen (Écoutez et répétez)

Jede Lektion beginnt mit **zwei Mini-Dialogen** zur selben Alltagssituation – einmal informell, einmal formell. Der Ablauf pro Dialog:

1. Der Coach **liest den Dialog vor** (Text-to-Speech / Audio-Ausgabe).
2. Anschließend wird jeder Satz einzeln angezeigt.
3. Der Nutzer **spricht den Satz nach** (Sprachaufnahme über Mikrofon).
4. Die Aufnahme wird **analysiert und ggf. korrigiert**:
   - Aussprache wird bewertet (korrekt / teilweise korrekt / zu überarbeiten).
   - Bei Fehlern wird der Satz erneut vorgesprochen und der Nutzer kann wiederholen.
   - Besondere Hinweise zu Ausspracheregeln werden gegeben (z.B. Liaison, stumme Endkonsonanten, Nasalvokale).

**Beispiel – Lektion 2 „Dire bonjour":**

*Teil A – Informell (tu):*
```
Coach liest vor:
  [1] Bonjour Paul !
  [2] Salut, Anne ! Comment vas-tu ?
  [3] Ça va ! Et toi ?
  [4] Ça va, merci !

→ Nutzer spricht Satz [1] nach → Coach bewertet Aussprache
→ Nutzer spricht Satz [2] nach → Coach bewertet Aussprache
→ ...
```

*Teil B – Formell (vous):*
```
Coach liest vor:
  [1] Bonsoir Madame Dupuis.
  [2] Bonsoir Monsieur Merle. Comment allez-vous ?
  [3] Je vais bien, merci, et vous ?
  [4] Très bien, merci !

→ Nutzer spricht nach und wird korrigiert
```

**Beispiel – Lektion 37 „Au restaurant":**

*Teil A – Informell (tu):*
```
  [1] Salut ! Tu veux manger quoi ?
  [2] Je sais pas… Qu'est-ce que tu me conseilles ?
  [3] Prends le plat du jour, il est super.
  [4] OK, je prends ça. Et toi ?
```

*Teil B – Formell (vous):*
```
  [1] Bonsoir Monsieur. Vous avez choisi ?
  [2] Oui, je voudrais le plat du jour, s'il vous plaît.
  [3] Très bien. Et comme boisson ?
  [4] Une carafe d'eau, s'il vous plaît.
```

### Schritt 2: Schriftliche Übungen (Pratiquez)

Nach dem Nachsprechen folgen **text- und auswahl-basierte Übungen**, die das Gelernte festigen. Auch die schriftlichen Übungen werden jeweils **in formeller und informeller Variante** angeboten, sodass der Nutzer beide Register trainiert. Die Übungstypen sind:

#### 2.1 Lückentexte (Complétez)
Der Nutzer ergänzt fehlende Wörter in Dialogen oder Sätzen. Die einzusetzenden Wörter werden als Auswahlliste vorgegeben.

**Beispiel – Lektion 2 (informell):**
```
Complétez le dialogue avec les mots suivants:
et toi – merci – ça va – salut

– __________ Isabelle, ça va ?
– __________, __________ ?
– Je vais bien, __________ !
```

**Beispiel – Lektion 2 (formell):**
```
Complétez le dialogue avec les mots suivants:
et vous – merci – allez – bonsoir

– __________ Madame. Comment __________-vous ?
– Je vais bien, __________, __________ ?
– Très bien, merci !
```

#### 2.2 Multiple-Choice (Cochez la bonne réponse)
Der Nutzer wählt aus mehreren Optionen die richtige Antwort.

**Beispiel – Lektion 3 „Dire au revoir":**
```
14h00 → 16h00
☐ À lundi !
☐ À demain !
☒ À tout à l'heure !
☐ À la semaine prochaine !
```

**Beispiel – Formell vs. Informell:**
```
Vous parlez à votre professeur. Que dites-vous ?
☐ Salut, ça va ?
☐ Eh, comment tu vas ?
☒ Bonjour Monsieur, comment allez-vous ?
☐ Coucou !
```

#### 2.3 Sätze ordnen (Mettez en ordre)
Der Nutzer bringt durcheinander geratene Dialogsätze in die richtige Reihenfolge. Jeweils einmal als informeller und einmal als formeller Dialog.

**Beispiel – Lektion 2 (informell):**
```
Mettez les phrases en ordre pour former un dialogue:
___ Ça va bien, merci.
___ Ça va, et toi ?
___ Bonjour Jules, ça va ?
___ Bonjour Anne !
```

**Beispiel – Lektion 2 (formell):**
```
Mettez les phrases en ordre pour former un dialogue:
___ Très bien, merci.
___ Bonsoir Madame Merle. Comment allez-vous ?
___ Je vais bien, merci. Et vous ?
___ Bonsoir Monsieur Renard.
```

#### 2.4 Zuordnungsübungen (Reliez)
Der Nutzer ordnet Elemente korrekt einander zu (z.B. maskuline/feminine Formen, formelle/informelle Entsprechungen, Silben zu Wörtern).

**Beispiel – Lektion 4 „L'état civil et la nationalité":**
```
Reliez pour former des phrases:
Marie est •         • français
                    • américaine
                    • japonaise
                    • grecque
Paul est •          • espagnol
                    • chinois
                    • turc
```

**Beispiel – Formell ↔ Informell zuordnen:**
```
Reliez chaque phrase informelle à son équivalent formel:
Salut !                    •    • Bonjour Monsieur / Madame.
Comment tu vas ?           •    • Comment allez-vous ?
Ça va, et toi ?            •    • Je vais bien, merci, et vous ?
Tchao !                    •    • Au revoir, Monsieur / Madame.
```

#### 2.5 Freie Antworten (Et vous? / Répondez)
Der Nutzer beantwortet persönliche Fragen schriftlich auf Französisch – einmal informell, einmal formell. Der Coach korrigiert Grammatik und Ausdruck.

**Beispiel – Lektion 4 (formell / vous):**
```
Répondez aux questions (formel):
a. Quel est votre nom ? _______________
b. Quel est votre prénom ? _______________
c. Vous êtes marié(e) ? _______________
d. Quelle est votre nationalité ? _______________
```

**Beispiel – Lektion 4 (informell / tu):**
```
Réponds aux questions (informel):
a. Comment tu t'appelles ? _______________
b. T'es marié(e) ? _______________
c. Tu viens d'où ? _______________
```

#### 2.6 Register-Transformation (Transformez)
Eine spezielle Übung, die den Wechsel zwischen formell und informell trainiert. Der Nutzer erhält einen Satz in einem Register und muss ihn in das andere umwandeln.

**Beispiel:**
```
Transformez en langage formel:
a. Salut, ça va ?
   → _______________________________________________
b. Tu veux un café ?
   → _______________________________________________

Transformez en langage informel:
c. Comment allez-vous, Madame ?
   → _______________________________________________
d. Pourriez-vous me passer le sel, s'il vous plaît ?
   → _______________________________________________
```

### Schritt 3: Grammatik-Zusammenfassung

Am Ende jeder Lektion zeigt der Coach eine kompakte **Grammatik-Box** mit den wichtigsten Regeln und Hinweisen der Lektion.

**Beispiel – Lektion 2:**
```
📖 Grammatik-Hinweis:
• formel → vous (Comment allez-vous ?)
• informel → tu (Comment vas-tu ?)

Vergleich:
  INFORMELL                    FORMELL
  Salut !                      Bonjour / Bonsoir Monsieur/Madame.
  Comment vas-tu ?             Comment allez-vous ?
  Ça va, et toi ?              Je vais bien, merci, et vous ?
  Salut ! / Tchao !            Au revoir, Monsieur/Madame.
```

**Beispiel – Lektion 4:**
```
📖 Le verbe ÊTRE:
AFFIRMATIF          NÉGATIF
je suis             je ne suis pas
tu es               tu n'es pas
il/elle est         il/elle n'est pas
nous sommes         nous ne sommes pas
vous êtes           vous n'êtes pas
ils/elles sont      ils/elles ne sont pas

💡 Aussprache-Hinweis:
• es / est = même prononciation
• vous_êtes (liaison: z)
• Am Wortende werden s und t nicht ausgesprochen.
```

### Fehlerkorrektur (stufenweise)

Bei allen Übungsformaten gilt folgende Strategie:
1. **Erster Fehler:** Der Coach gibt einen Hinweis, ohne die Lösung zu verraten (z.B. „Attention au genre du mot" / „Achte auf das Geschlecht des Wortes").
2. **Zweiter Fehler bei derselben Aufgabe:** Der Coach korrigiert direkt, zeigt die richtige Antwort und erklärt die zugrunde liegende Regel.

Bei der **Aussprachebewertung** (Schritt 1) wird hingegen sofort korrigiert, da mündliche Fehler sich sonst einschleifen.

---

## Funktion 3: Erfolge kontrollieren

### Beschreibung
Der Nutzer kann jederzeit seinen Lernfortschritt einsehen. Die Erfolgskontrolle umfasst zwei Bereiche.

### 3.1 Fehleranalyse
- Der Coach führt Buch über die Fehler des Nutzers (Kategorie, Häufigkeit, betroffene Lektionen/Themen).
- Auf Anfrage erstellt der Coach eine Übersicht der häufigsten Fehlerquellen.
- Der Coach schlägt gezielt Übungen oder Wiederholungs-Lektionen vor, die an den Schwachstellen ansetzen.
- Beispielausgabe:

```
Häufigste Fehler:
1. Verwechslung formell/informell – tu vs. vous (Lektionen 2, 7)
2. Nationalitäten – maskulin/feminin (Lektion 4)
3. Zahlen über 60 (Lektion 9)

Empfehlung: Lektionen 2 und 4 wiederholen, Fokus auf Genus-Übungen.
```

### 3.2 Niveau-Einschätzung
- Der Coach schätzt basierend auf den bisherigen Übungsergebnissen das aktuelle Sprachniveau des Nutzers ein (A1–C2).
- Die Einschätzung berücksichtigt Grammatik, Wortschatz, Aussprache und Verständnis separat.
- Bei deutlicher Verbesserung schlägt der Coach vor, das Übungsniveau anzupassen.
- Beispielausgabe:

```
Aktuelle Niveau-Einschätzung:
- Grammatik: A2
- Wortschatz: A2
- Aussprache: A1
- Verständnis: A2

Gesamteinschätzung: A1/A2 (Übergang)
Empfehlung: Aussprache-Training intensivieren – mehr Dialoge nachsprechen.
```

### 3.3 Zwischentests (Bilan)

Nach jedem thematischen Block bietet der Coach einen **Zwischentest (Bilan)** an, der die Inhalte der vorangegangenen Lektionen abprüft. Der Bilan kombiniert:
- Nachsprechen ausgewählter Sätze aus den bisherigen Dialogen
- Lückentexte und Multiple-Choice-Aufgaben
- Eine kurze freie Dialogsimulation zum Blockthema

Das Ergebnis fließt in die Fehleranalyse und Niveau-Einschätzung ein.

---

## Navigation und Interaktion

Der Coach bietet dem Nutzer zu Beginn jeder Session ein Hauptmenü an:

```
Bonjour [Name]! Que voulez-vous faire aujourd'hui?

1. Créer un plan d'entraînement (Trainingsplan erstellen)
2. Pratiquer – Leçon [nächste Lektion] (Interaktiv üben)
3. Voir mes progrès (Erfolge kontrollieren)
```

Der Coach zeigt automatisch die **nächste unbearbeitete Lektion** als Vorschlag an. Der Nutzer kann aber auch eine beliebige frühere Lektion wiederholen oder eine spätere vorziehen.

Innerhalb jeder Lektion wird der Fortschritt angezeigt, inklusive der aktuellen Register-Variante:
```
Leçon 2 – Dire bonjour
[■■□□□□] Schritt 1a/3: Écoutez et répétez (informell – tu)

Leçon 2 – Dire bonjour
[■■■□□□] Schritt 1b/3: Écoutez et répétez (formell – vous)
```

---

## Technische Anforderungen

### Sprachaufnahme und Aussprachebewertung
- Die App muss Zugriff auf das **Mikrofon** des Nutzers haben.
- Aufgenommene Sprache wird per **Speech-to-Text** transkribiert und mit dem Zieltext verglichen.
- Idealerweise wird auch die **Aussprachequalität** bewertet (Intonation, Betonung, Liaison).
- Feedback erfolgt unmittelbar nach jeder Aufnahme.

### Text-to-Speech
- Alle Dialoge und Beispielsätze sollen **vorgelesen** werden können (natürliche französische Stimme).
- Die Geschwindigkeit soll anpassbar sein (langsam für Anfänger, normal für Fortgeschrittene).

---

## Zusammenfassung der Konfiguration

| Eigenschaft | Wert |
|---|---|
| Kommunikationssprache | Französisch (Deutsch nur bei niedrigem Niveau für Erklärungen) |
| Ton | Sachlich-neutral |
| Sprachniveau | Flexibel wählbar (A1–C2), Start-Empfehlung A1 |
| Trainingsplan-Eingaben | Zielniveau (Pflicht), Grammatik-Schwerpunkte (Optional), Themenvorgaben (Optional), Zeitbudget (Pflicht) |
| Trainingsplan | 65 Lektionen, geordnet nach Alltagssituationen, individuell priorisiert nach Ziel, Schwerpunkten und Themen |
| Zeitplanung | Zeitbasiert (Minuten/Tag, Tage/Woche) |
| Register-Varianten | Jede Übung wird in formeller (vous) und informeller (tu) Variante durchgeführt |
| Lektionsablauf | 1. Dialog hören & nachsprechen (informell + formell) → 2. Schriftliche Übungen (informell + formell) → 3. Grammatik-Box |
| Übungstypen | Nachsprechen (mit Aufnahme), Lückentexte, Multiple-Choice, Sätze ordnen, Zuordnung, freie Antworten, Register-Transformation |
| Aussprachebewertung | Sprachaufnahme mit automatischer Korrektur |
| Fehlerkorrektur (schriftlich) | Stufenweise (erst Hinweis, dann direkte Korrektur) |
| Fehlerkorrektur (mündlich) | Sofortige Korrektur bei Aussprachefehlern |
| Erfolgskontrolle | Fehleranalyse, Niveau-Einschätzung, Zwischentests (Bilan) |
| Gedächtnis | Persistent (Name, Niveau, Fortschritte, Fehlerhistorie über Sessions) |
| Begleitend | 30 wichtige Verben im Präsens, systematisch über die Lektionen verteilt |
