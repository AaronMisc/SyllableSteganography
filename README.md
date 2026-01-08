# Syllable Steganography
Encode hidden messages in plain text, by counting the syllables.

## 📋Terms
### Word Group Size (W)
A word group size is how many words are in a word group. Each word group has its syllables counted. Represented as W.
Word group size: 2. 

**Example sentence**: (Words are) (grouped into) (twos watermelon).
**Syllables**: (2) (3) (5).

### Binary Group Size (B)
How many binary bits there are per ID.

The greater B is, the more number of IDs in the key.
Number of IDs = $2 ^ B$.
However, it means more words have to be used to encode a secret message.

<details>
	<summary><strong>Examples</strong></summary>
	<h4>B = 2</h4>
	<p>If B = 2, there would be 2<sup>2</sup> = 4 IDs.</p>
	<p>So an example key might be:</p>
	<ul>
		<li>0 &rarr; abcdef</li>
		<li>1 &rarr; ghijkl</li>
		<li>2 &rarr; mnopqrs</li>
		<li>3 &rarr; tuvwxyz</li>
	</ul>
	<p>Good luck decoding that.</p>
	<h4>B = 4</h4>
	<p>However, if B = 4, this would give 2<sup>4</sup> = 16 IDs.</p>
	<p>This means for every ID there would be about <sup>26</sup>&frasl;<sub>16</sub> = 1.625 characters.</p>
	<p>An example key is shown below.</p>
	<p>This is recommended.</p>
</details>

### Key
Something that maps characters to numbers (IDs). Example: See below.
Multiple characters can map to one ID. Example: abc -> 12.
**Warning**: To use the encoder, there can't be multiple IDs that map to the same character. 12 -> b and 5 -> b would be invalid. This is valid for manual encoding.

## 🔒Encoding
Example message: HI
1. Pick a word group size (W) and binary group size (B). Example: W = 4. B = 4.
2. Make a key with 2^B IDs. Example: 16 IDs. See the one shown below.
3. Encode your message using that key. For each letter, get the number for it using the key. Example: 74.
4. Convert the numbers to binary with B places. Example: 0111, 0100.
5. Go through each of the numbers. Make a word group with size W for each.
	- **0** means **even** number of syllables. Example: Today I went shopping
	- **1** means **odd** number of syllables. Example: at the local store. 
6. Put the word groups together to get your final encoded message! Example: Today I went shopping at the local store. I started acting strangely which was kinda dumb. I ate some food from the pyrotechnics store and now I'm stuffed. It was real fun.

## 🔐Decoding
### Code
1. Put the encoding key into the characters to csv file (characters_to_id.csv).
2. Change the constants at the beginning of the code (under configuration) to change global settings.
3. Paste the secret message into string.
```python
string = """Today I went shopping at the local store. I started acting strangely which was kinda dumb. I ate some food from the pyrotechnics store and now I'm stuffed. It was real fun."""
decoded = steganography_decode_string(string, ID_TO_CHARACTERS)
print(decoded)
```

2. Use the decoded message to guess the original word.
3. Look through the words and syllables in the output to see if there are any errors.
```
to-day 2
i 1
went 1
shop-ping 2
...
```
4. If there are, go to the syllable overrides csv file (syllable_overrides.csv) and add a line with this format: word;syllables.

<details>
	<summary><strong>Manually</strong></summary>
	<ol>
		<li>Get the word group size (<strong>W</strong>), the binary group size (<strong>B</strong>), and the key.
			<p>Example: W = 4, B = 4. The key is provided below.</p>
		</li>
		<li>Group the words into groups of size <strong>W</strong>.
			<p>Example: (Today I went shopping) (at the local store.)</p>
		</li>
		<li>Count the syllables in each group.
			<p>Example: (6) (5)</p>
		</li>
		<li>Convert syllables to bits.
			<ul>
				<li>Even number of syllables means <strong>0</strong>. Example: 6 &rarr; 0</li>
				<li>Odd number of syllables means <strong>1</strong>. Example: 5 &rarr; 1</li>
			</ul>
		</li>
		<li>Group the bits into groups of size <strong>B</strong>.
			<p>Example: (0, 1, 1, 1), (0, 1, 0, 0)</p>
		</li>
		<li>Convert the binary numbers into the base of the key.
			<p>Example: 7, 4</p>
		</li>
		<li>Decode the values using the key.
			<p>Example: h, i</p>
		</li>
		<li>Each set of characters represents possible values. Use them to infer the word.
			<ol>
				<li>Example sets: vkj, cu, mw, ypb.</li>
				<li>Since there must be at least one vowel, either <strong>U</strong> or <strong>Y</strong> is correct.</li>
				<li>If it is <strong>Y</strong>, then <strong>U</strong> should also appear, because three consonants in a row with Y is unlikely.</li>
				<li>The first letter is probably <strong>J</strong>, based on the second letter being <strong>U</strong>.</li>
				<li>The third letter being <strong>W</strong> would form <strong>JUW</strong>, which is unlikely, so it is <strong>M</strong>.</li>
				<li>The last letter is clearly <strong>P</strong>.</li>
				<li>Combining the letters:
					<p>J from the first, U from the second, M from the third, and P from the fourth.</p>
					<p>The word is <strong>JUMP</strong>.</p>
				</li>
			</ol>
		</li>
	</ol>
</details>

## Pros and Cons of this Steganography Method
### ✔️Pros
- Works in speech.
- Hard to detect.

### ❌Cons
- Low data rate.
- Requires preparation.
- Have to add overrides manually for code.

## 🔑Keys
To make a key, use the CSV. For easier editing, open in a spreadsheet editor.

This key uses English letter frequency to prevent commonly used letters from being guessed.
**Here is an example of a key in CSV format:**  
e;0 (This means that e is decoded as 0)  
t;1  
a;2  
o;3  
i;4  
n;5  
s;6  
h;7  
r;8  
dl;9 (There can be multiple letters per id)  
cu;10  
mw;11  
fg;12  
ypb;13  
vkj;14  
xqz;15 (Has 16 items, because syllables are grouped into 4s, so there will be 2^4=16 possibilities)
