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
7. [Troubleshooting](#troubleshooting)

## Installation & Setup

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- A web server (optional, for local development)

### Setup Instructions

1. **Clone or download the project files:**
   ```
   /workspace/
   ├── index.html
   ├── main.js
   ├── style.css
   └── sound.mp3 (optional audio file)
   ```

2. **Open the application:**
   - For local development: Open `index.html` directly in your browser
   - For production: Serve the files through a web server

3. **Optional: Add audio file**
   - Place a `sound.mp3` file in the same directory for alarm sound
   - If no audio file is present, the alarm will still trigger with a browser alert

## HTML Structure

### Document Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>11715</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Main container with form -->
    <div class="container">
        <h1>Alarm</h1>
        <form>
            <label for="input-time">Enter time (hours:minutes:seconds):</label>
            <input type="text" id="input-time" name="input-time" placeholder="00:00:00" required>
            <button type="button" id="start-button">Start</button>
        </form>
    </div>
    
    <!-- Countdown display -->
    <div class="countdown-container">
        <span id="countdown-timer"></span>
    </div>
    
    <script src="main.js"></script>
</body>
</html>
```

### DOM Elements

| Element ID | Type | Purpose | Attributes |
|------------|------|---------|------------|
| `input-time` | `<input>` | Time input field for user to enter countdown duration | `type="text"`, `placeholder="00:00:00"`, `required` |
| `start-button` | `<button>` | Button to initiate the countdown timer | `type="button"` |
| `countdown-timer` | `<span>` | Display element showing remaining time | None |

### Form Structure
- **Form Type**: Standard HTML form (no submission)
- **Input Format**: Time in `HH:MM:SS` format
- **Validation**: Required field validation
- **Button Action**: JavaScript event handler (not form submission)

## CSS Classes & Styling

### Layout Classes

#### `.container`
- **Purpose**: Main application container
- **Styling**:
  - Background: Light pink (`#fff7f7`)
  - Border: Dark gray (`#252525`)
  - Border radius: 5px
  - Padding: 20px
  - Margin: 20px

#### `.countdown-container`
- **Purpose**: Container for countdown timer display
- **Styling**:
  - Flexbox layout (centered)
  - Margin-top: 30px

### Typography Classes

#### `h1`
- **Purpose**: Main application title
- **Styling**:
  - Color: Dark gray (`#333`)
  - Font size: 36px
  - Font weight: Bold
  - Text alignment: Center
  - Margin-top: 0

#### `label`
- **Purpose**: Form label text
- **Styling**:
  - Color: Dark gray (`#333`)
  - Font size: 20px
  - Margin-bottom: 10px

### Form Elements

#### `input`
- **Purpose**: Time input field styling
- **Styling**:
  - Font size: 18px
  - Padding: 10px
  - Border: Light gray (`#ccc`)
  - Border radius: 5px
  - Text alignment: Center
  - Width: 200px

#### `button`
- **Purpose**: Start button styling
- **Styling**:
  - Background: Dark (`#141414`)
  - Color: Light gray (`rgb(235, 231, 231)`)
  - Padding: 10px 20px
  - Font size: 18px
  - Border radius: 5px
  - Width: 150px
  - Cursor: Pointer

### Display Elements

#### `#countdown-timer`
- **Purpose**: Countdown timer display
- **Styling**:
  - Color: Dark gray (`#333`)
  - Font size: 64px
  - Font weight: Bold
  - Text alignment: Center
  - Border: Black (`#000000`)
  - Border radius: 5px
  - Padding: 20px
  - Width: 300px

### Global Styles

#### `body, html`
- **Purpose**: Global layout configuration
- **Styling**:
  - Width/Height: 100%
  - Display: Flexbox column
  - Justify content: Center
  - Align items: Center

## JavaScript API

### Global Variables

#### `startButton`
- **Type**: `HTMLElement`
- **Purpose**: Reference to the start button DOM element
- **Access**: `document.getElementById("start-button")`

#### `timeInput`
- **Type**: `HTMLElement`
- **Purpose**: Reference to the time input field DOM element
- **Access**: `document.getElementById("input-time")`

#### `countdownInterval`
- **Type**: `number` (setInterval ID)
- **Purpose**: Stores the interval ID for the countdown timer
- **Scope**: Global variable for interval management

### Public Functions

#### `startCountdown()`
- **Purpose**: Initiates the countdown timer
- **Parameters**: None
- **Returns**: `undefined`
- **Side Effects**:
  - Clears any existing countdown interval
  - Starts a new countdown timer
  - Updates the countdown display every second
  - Triggers alarm when timer expires

**Implementation Details:**
```javascript
function startCountdown() {
  clearInterval(countdownInterval);
  const countDownTime = new Date().getTime() + getTimeInMilliseconds(timeInput.value);
  countdownInterval = setInterval(function() {
    const now = new Date().getTime();
    const distance = countDownTime - now;
    if (distance < 0) {
      clearInterval(countdownInterval);
      playSound();
      window.alert("Time is up!");
    } else {
      const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);
      document.getElementById("countdown-timer").innerHTML = `${hours}h : ${minutes}m : ${seconds}s`;
    }
  }, 1000);
}
```

#### `getTimeInMilliseconds(timeString)`
- **Purpose**: Converts time string to milliseconds
- **Parameters**:
  - `timeString` (string): Time in "HH:MM:SS" format
- **Returns**: `number` - Time in milliseconds
- **Throws**: May throw if timeString format is invalid

**Implementation Details:**
```javascript
function getTimeInMilliseconds(timeString) {
  const [hours, minutes, seconds] = timeString.split(":");
  return (parseInt(hours) * 60 * 60 + parseInt(minutes) * 60 + parseInt(seconds)) * 1000;
}
```

**Example Usage:**
```javascript
getTimeInMilliseconds("01:30:45"); // Returns 5445000 (1 hour, 30 minutes, 45 seconds in ms)
getTimeInMilliseconds("00:05:00"); // Returns 300000 (5 minutes in ms)
```

#### `playSound()`
- **Purpose**: Plays the alarm sound
- **Parameters**: None
- **Returns**: `undefined`
- **Side Effects**: Attempts to play audio file

**Implementation Details:**
```javascript
function playSound() {
  const audio = new Audio("sound.mp3");
  audio.play();
}
```

**Note**: This function will fail silently if `sound.mp3` is not present or if the browser blocks autoplay.

### Event Listeners

#### Start Button Click Event
- **Element**: `startButton`
- **Event**: `click`
- **Handler**: `startCountdown`
- **Purpose**: Initiates countdown when user clicks the start button

**Implementation:**
```javascript
startButton.addEventListener("click", startCountdown);
```

## Usage Examples

### Basic Usage

1. **Setting a 5-minute timer:**
   ```
   Input: 00:05:00
   Click: Start button
   Result: Countdown displays "0h : 5m : 0s" and decreases
   ```

2. **Setting a 1-hour timer:**
   ```
   Input: 01:00:00
   Click: Start button
   Result: Countdown displays "1h : 0m : 0s" and decreases
   ```

3. **Setting a complex timer:**
   ```
   Input: 02:15:30
   Click: Start button
   Result: Countdown displays "2h : 15m : 30s" and decreases
   ```

### Programmatic Usage

#### Starting a Timer Programmatically
```javascript
// Set the input value
document.getElementById("input-time").value = "00:10:00";

// Start the countdown
startCountdown();
```

#### Converting Time to Milliseconds
```javascript
// Convert various time formats
const fiveMinutes = getTimeInMilliseconds("00:05:00");
const oneHour = getTimeInMilliseconds("01:00:00");
const complexTime = getTimeInMilliseconds("02:30:45");
```

#### Playing Sound Manually
```javascript
// Trigger alarm sound
playSound();
```

### Advanced Usage Examples

#### Creating Multiple Timers (Custom Implementation)
```javascript
// Example of how you might extend the functionality
class TimerManager {
  constructor() {
    this.timers = new Map();
  }
  
  createTimer(id, duration) {
    const timerId = setInterval(() => {
      // Timer logic here
    }, 1000);
    this.timers.set(id, timerId);
  }
  
  stopTimer(id) {
    const timerId = this.timers.get(id);
    if (timerId) {
      clearInterval(timerId);
      this.timers.delete(id);
    }
  }
}
```

#### Custom Time Format Validation
```javascript
function validateTimeFormat(timeString) {
  const timeRegex = /^([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2})$/;
  if (!timeRegex.test(timeString)) {
    throw new Error("Invalid time format. Use HH:MM:SS");
  }
  
  const [hours, minutes, seconds] = timeString.split(":").map(Number);
  
  if (minutes >= 60 || seconds >= 60) {
    throw new Error("Minutes and seconds must be less than 60");
  }
  
  return true;
}
```

## Browser Compatibility

### Supported Browsers
- **Chrome**: 60+ (Full support)
- **Firefox**: 55+ (Full support)
- **Safari**: 12+ (Full support)
- **Edge**: 79+ (Full support)

### Required Features
- **ES6+ JavaScript**: Arrow functions, const/let, template literals
- **DOM API**: getElementById, addEventListener
- **Audio API**: Audio constructor and play() method
- **CSS Flexbox**: For layout styling

### Known Limitations
- **Audio Autoplay**: Some browsers may block audio autoplay without user interaction
- **Mobile Browsers**: May have different audio behavior
- **Time Format**: Only supports HH:MM:SS format (24-hour)

## Troubleshooting

### Common Issues

#### Timer Not Starting
**Problem**: Clicking start button doesn't initiate countdown
**Solutions**:
1. Check browser console for JavaScript errors
2. Verify input format is HH:MM:SS
3. Ensure input field is not empty
4. Check if JavaScript is enabled

#### Audio Not Playing
**Problem**: No sound when timer expires
**Solutions**:
1. Verify `sound.mp3` file exists in the same directory
2. Check browser audio permissions
3. Ensure user has interacted with the page before timer expires
4. Try different audio formats (MP3, WAV, OGG)

#### Display Issues
**Problem**: Countdown timer not displaying correctly
**Solutions**:
1. Check CSS file is loaded properly
2. Verify browser supports CSS Flexbox
3. Clear browser cache and reload
4. Check for CSS conflicts

#### Time Format Errors
**Problem**: Invalid time format causing errors
**Solutions**:
1. Use exactly HH:MM:SS format (e.g., "01:30:45")
2. Ensure all numbers are two digits with leading zeros
3. Don't use spaces or other characters
4. Maximum time: 99:59:59

### Debugging Tips

#### Enable Console Logging
```javascript
// Add this to debug timer functionality
function startCountdown() {
  console.log("Starting countdown with:", timeInput.value);
  clearInterval(countdownInterval);
  const countDownTime = new Date().getTime() + getTimeInMilliseconds(timeInput.value);
  console.log("Countdown will end at:", new Date(countDownTime));
  // ... rest of function
}
```

#### Check Audio Support
```javascript
// Test audio functionality
function testAudio() {
  try {
    const audio = new Audio("sound.mp3");
    audio.play().then(() => {
      console.log("Audio playback successful");
    }).catch(error => {
      console.error("Audio playback failed:", error);
    });
  } catch (error) {
    console.error("Audio creation failed:", error);
  }
}
```

---

## License

This project is open source. Feel free to modify and distribute as needed.

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review browser compatibility requirements
3. Test in different browsers and environments
4. Check browser console for error messages