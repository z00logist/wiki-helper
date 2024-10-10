# Wiki Helper

Wiki Helper Widget is a Q&A bot designed specifically for Wikipedia. It allows you to interact with a trained model directly within Wikipedia pages, providing answers based on the content of the article you’re reading. This widget makes it easy to get quick answers without leaving the page.

## Features:
- **Automatic model training** based on the Wikipedia article you are viewing.
- **Ask questions** directly related to the article content.
- **Seamless experience** with a toggle button for quick access.

### Notes
- This widget only works within **Wikipedia** pages.
- Currently, it supports only **English language** Q&A.

## Installation Guide

### Step 0: Run the service
1. Clone this repository on your computer.
2. Prepare your environment via `make prepare`.
3. Run the service via `make run`.

### Step 1: Install the Chrome Extension

1. Open Chrome and go to the `Extensions` page by typing `chrome://extensions/` in your address bar.
2. Turn on **Developer mode** (toggle in the top right corner).
3. Click **Load unpacked** and select the folder in this project [widget extension](widget_extension).
4. You should now see the Wiki Helper icon in your Chrome toolbar.

### Step 2: Using the Widget

1. **Navigate to any Wikipedia page**.
2. **Click the Wiki Helper button** (visible in your browser toolbar) to toggle the widget window open. This is a simple interface that will appear on the side of your Wikipedia page.

![UI Overview](assets/UI.gif)

### Step 3: Asking Questions

Once you've opened a Wikipedia article, you can begin interacting with the bot. Here's how it works:

#### 1. Bot Reads the Article

When you ask your first question, the bot will automatically read and process the article in the background. Simply input your query, and the bot will use the content of the article to answer.

![Reading Article](assets/read.gif)

#### 2. Bot Answers Your Question

After processing the article, the bot will respond with answers based on the article's content. You can ask follow-up questions, and the bot will continue to reference the same article for context.

![Asking Questions](assets/communication.gif)

Now, you're ready to explore Wikipedia with the power of automated, contextual Q&A!

## Developer Guide

For advanced usage and instructions on running the service locally, refer to the [Developer Guide](examples/README.md).
