# Binding of Isaac Episode Data Extractor
Scrapes data from a given episode from Northernlion's decade-long Binding of Isaac Series. 

## Planned Features

* Basic Episode Data
    * Binding of Isaac Version (Rebirth, Afterbirth, Afterbirth+, Repentence)
    * Episode Title
    * Episode Number
    * Runtime
    * Release Date
    * Audio clip of "eyy everybody"
* Advanced Run Data
    * Episode result (win/loss)
        * Ending achieved (if win)
    * Seed
    * Character

## To Do

- [ ] Write findResult method to determine win/loss
- [ ] Write findSeedAndCharacter method to read video beginning
- [ ] Write intro method to extract "eyy everybody" clip
- [ ] Tune threshold variables for findResult, findSeedAndCharacter OpenCV methods

## Dependencies

Dependencies can be installed via pip install -r dependencies.txt

