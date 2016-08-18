# QA

Test your .glyphs files for common errors.

## Want to test against your own criterea?
No problem! font attributes such as license, copyright etc are defined in the 'qa.yml' file.
![alt tag](config_file.png)

## Apart from meta data, what else does it check?
### Glyphs:
- Duplicate glyphs
- Space and nbspace share same width

### Vertical Metrics:
- Do metrics match Google Fonts legacy 125% spec.
- Do metrics match Google Fonts Khaled's schema.
- Do metrics match Google Fonts Kalapi's schema.

## Why bother?
Manually checking fonts is a pain. If we can store all the constants which will not change in a yml file. We can simply run our tests and discover if anything has changed or is incorrect. 

## How did this project start?
The Google Fonts collection is currently over 800 fonts. We needed a way to quickly assess if certain families are not meeting our new specification.

## Want to contribute?
By all means submit an issue or pull request. 