# Alarm Timer Application - API Documentation

## Overview

This is a web-based alarm timer application that allows users to set countdown timers and receive audio notifications when the timer expires. The application is built using vanilla HTML, CSS, and JavaScript.

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [HTML Structure](#html-structure)
3. [CSS Classes & Styling](#css-classes--styling)
4. [JavaScript API](#javascript-api)
5. [Usage Examples](#usage-examples)
6. [Browser Compatibility](#browser-compatibility)
7. [Dependencies](#dependencies)

## Installation & Setup

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- A web server (optional, for local development)

### Setup Instructions

1. **Clone or download the project files:**
   ```bash
   # Ensure you have these files in your project directory:
   # - index.html
   # - main.js
   # - style.css
   # - sound.mp3 (optional audio file)
   ```

2. **Open the application:**
   - For local development: Open `index.html` directly in your browser
   - For production: Serve the files through a web server

3. **Optional: Add audio file**
   - Place a `sound.mp3` file in the same directory as `index.html`
   - The application will play this sound when the timer expires

## HTML Structure

### Main Elements

#### `<div class="container">`
The main container for the alarm input interface.

**Attributes:**
- `class`: "container" - Applies container styling

**Child Elements:**
- `<h1>`: Application title
- `<form>`: Input form for time setting

#### `<h1>Alarm</h1>`
The main application title.

#### `<form>`
The input form for setting the alarm time.

**Child Elements:**
- `<label>`: Input label
- `<input>`: Time input field
- `<button>`: Start button

#### `<input type="text" id="input-time">`
The time input field where users enter the countdown duration.

**Attributes:**
- `id`: "input-time" - Unique identifier for JavaScript access
- `name`: "input-time" - Form field name
- `placeholder`: "00:00:00" - Placeholder text showing expected format
- `required`: Required field validation

**Expected Format:** `HH:MM:SS` (hours:minutes:seconds)

#### `<button type="button" id="start-button">Start</button>`
The button that initiates the countdown timer.

**Attributes:**
- `id`: "start-button" - Unique identifier for JavaScript access
- `type`: "button" - Prevents form submission

#### `<div class="countdown-container">`
Container for displaying the countdown timer.

**Attributes:**
- `class`: "countdown-container" - Applies countdown styling

**Child Elements:**
- `<span id="countdown-timer">`: The countdown display element

#### `<span id="countdown-timer"></span>`
The element that displays the current countdown time.

**Attributes:**
- `id`: "countdown-timer" - Unique identifier for JavaScript access

## CSS Classes & Styling

### Global Styles

#### `body, html`
Sets up the main page layout.

**Properties:**
- `width: 100%` - Full width
- `height: 100%` - Full height
- `display: flex` - Flexbox layout
- `flex-flow: column wrap` - Column direction with wrapping
- `justify-content: center` - Center content horizontally
- `align-items: center` - Center content vertically

### Component Classes

#### `.container`
Styles the main application container.

**Properties:**
- `background-color: #fff7f7` - Light pink background
- `border: 1px solid #252525` - Dark border
- `border-radius: 5px` - Rounded corners
- `padding: 20px` - Internal spacing
- `margin: 20px` - External spacing

#### `h1`
Styles the main title.

**Properties:**
- `color: #333` - Dark gray text
- `font-size: 36px` - Large font size
- `font-weight: bold` - Bold text
- `text-align: center` - Centered text
- `margin-top: 0` - No top margin

#### `form`
Styles the input form.

**Properties:**
- `display: flex` - Flexbox layout
- `flex-direction: column` - Vertical layout
- `align-items: center` - Center items horizontally

#### `label`
Styles form labels.

**Properties:**
- `color: #333` - Dark gray text
- `font-size: 20px` - Medium font size
- `margin-bottom: 10px` - Bottom spacing

#### `input`
Styles input fields.

**Properties:**
- `font-size: 18px` - Medium font size
- `padding: 10px` - Internal spacing
- `border: 1px solid #ccc` - Light gray border
- `border-radius: 5px` - Rounded corners
- `text-align: center` - Centered text
- `width: 200px` - Fixed width

#### `button`
Styles buttons.

**Properties:**
- `background-color: #141414` - Dark background
- `border: none` - No border
- `color: rgb(235, 231, 231)` - Light text
- `padding: 10px 20px` - Internal spacing
- `text-align: center` - Centered text
- `text-decoration: none` - No text decoration
- `font-size: 18px` - Medium font size
- `margin-top: 10px` - Top spacing
- `cursor: pointer` - Pointer cursor on hover
- `border-radius: 5px` - Rounded corners
- `width: 150px` - Fixed width

#### `.countdown-container`
Styles the countdown display container.

**Properties:**
- `display: flex` - Flexbox layout
- `justify-content: center` - Center horizontally
- `align-items: center` - Center vertically
- `margin-top: 30px` - Top spacing

#### `#countdown-timer`
Styles the countdown timer display.

**Properties:**
- `color: #333` - Dark gray text
- `font-size: 64px` - Large font size
- `font-weight: bold` - Bold text
- `text-align: center` - Centered text
- `border: 1px solid #000000` - Black border
- `border-radius: 5px` - Rounded corners
- `padding: 20px` - Internal spacing
- `width: 300px` - Fixed width

## JavaScript API

### Global Variables

#### `startButton`
Reference to the start button DOM element.

**Type:** `HTMLElement`
**Access:** `document.getElementById("start-button")`

#### `timeInput`
Reference to the time input field DOM element.

**Type:** `HTMLElement`
**Access:** `document.getElementById("input-time")`

#### `countdownInterval`
Stores the interval ID for the countdown timer.

**Type:** `number | undefined`
**Initial Value:** `undefined`

### Functions

#### `startCountdown()`
Initiates the countdown timer based on the input time.

**Parameters:** None

**Returns:** `void`

**Behavior:**
1. Clears any existing countdown interval
2. Calculates the target time by adding input duration to current time
3. Sets up a 1-second interval to update the countdown display
4. When countdown reaches zero, plays sound and shows alert

**Example:**
```javascript
// This function is called when the start button is clicked
startCountdown();
```

#### `getTimeInMilliseconds(timeString)`
Converts a time string in HH:MM:SS format to milliseconds.

**Parameters:**
- `timeString` (string): Time in "HH:MM:SS" format

**Returns:** `number` - Time duration in milliseconds

**Example:**
```javascript
const duration = getTimeInMilliseconds("01:30:45");
// Returns: 5445000 (1 hour, 30 minutes, 45 seconds in milliseconds)
```

**Error Handling:**
- If the time string format is invalid, the function may return `NaN`
- Ensure the input follows the exact "HH:MM:SS" format

#### `playSound()`
Plays an audio notification when the timer expires.

**Parameters:** None

**Returns:** `void`

**Behavior:**
1. Creates a new Audio object pointing to "sound.mp3"
2. Attempts to play the audio file
3. If the audio file doesn't exist, the function will fail silently

**Example:**
```javascript
playSound(); // Plays the alarm sound
```

**Requirements:**
- Requires a `sound.mp3` file in the same directory as `index.html`
- Browser must support HTML5 Audio API
- User interaction may be required for audio to play (browser autoplay policies)

### Event Listeners

#### Start Button Click Event
Attached to the start button to initiate countdown.

**Event:** `click`
**Element:** `startButton`
**Handler:** `startCountdown`

**Example:**
```javascript
startButton.addEventListener("click", startCountdown);
```

## Usage Examples

### Basic Usage

1. **Open the application** in your web browser
2. **Enter a time** in the input field using HH:MM:SS format (e.g., "00:05:00" for 5 minutes)
3. **Click the Start button** to begin the countdown
4. **Watch the countdown** display update every second
5. **Receive notification** when the timer expires (audio + alert)

### Time Format Examples

```javascript
// Valid time formats:
"00:01:00"  // 1 minute
"00:05:30"  // 5 minutes 30 seconds
"01:00:00"  // 1 hour
"02:30:45"  // 2 hours 30 minutes 45 seconds
"00:00:10"  // 10 seconds
```

### Programmatic Usage

```javascript
// Set a timer programmatically
timeInput.value = "00:02:00"; // Set 2 minutes
startCountdown(); // Start the countdown

// Check current countdown status
if (countdownInterval) {
    console.log("Countdown is running");
} else {
    console.log("No countdown active");
}

// Stop current countdown
if (countdownInterval) {
    clearInterval(countdownInterval);
    countdownInterval = undefined;
}
```

### Custom Styling Example

```css
/* Custom theme example */
.container {
    background-color: #2c3e50;
    border-color: #34495e;
}

h1 {
    color: #ecf0f1;
}

button {
    background-color: #e74c3c;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #c0392b;
}
```

## Browser Compatibility

### Supported Browsers
- **Chrome:** 60+
- **Firefox:** 55+
- **Safari:** 12+
- **Edge:** 79+

### Required Features
- HTML5 Audio API
- ES6+ JavaScript features
- CSS Flexbox
- DOM manipulation APIs

### Known Limitations
- Audio autoplay may be blocked by browser policies
- Some older browsers may not support all CSS features
- Mobile browsers may have different audio behavior

## Dependencies

### Required Files
- `index.html` - Main HTML structure
- `main.js` - JavaScript functionality
- `style.css` - CSS styling

### Optional Files
- `sound.mp3` - Audio notification file

### External Dependencies
- None (pure vanilla JavaScript, HTML, CSS)

### Browser APIs Used
- `document.getElementById()` - DOM element access
- `setInterval()` - Timer functionality
- `clearInterval()` - Timer cleanup
- `Date.getTime()` - Time calculations
- `Audio()` - Sound playback
- `addEventListener()` - Event handling

## Troubleshooting

### Common Issues

1. **Timer not starting:**
   - Check that the time format is correct (HH:MM:SS)
   - Ensure the input field has a value
   - Verify JavaScript is enabled

2. **Audio not playing:**
   - Ensure `sound.mp3` exists in the same directory
   - Check browser audio permissions
   - Try clicking the page first (user interaction required)

3. **Styling issues:**
   - Verify `style.css` is properly linked
   - Check browser compatibility
   - Ensure no CSS conflicts

4. **Countdown not updating:**
   - Check browser console for JavaScript errors
   - Verify the countdown timer element exists
   - Ensure no other scripts are interfering

### Debug Mode

To enable debug logging, add this to your browser console:

```javascript
// Override the original function to add logging
const originalStartCountdown = startCountdown;
startCountdown = function() {
    console.log("Starting countdown with time:", timeInput.value);
    originalStartCountdown();
};
```

## License

This project is open source and available under the MIT License.