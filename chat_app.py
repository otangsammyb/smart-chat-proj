from uuid import uuid4
from datetime import datetime
from nicegui import ui

# Define the initial messages list with an extra field for username and timestamp
messages = []

# Define the theme colors for the app
message_bg_color = '#32CD32'  # Green for chat messages
app_bg_color = '#333333'  # Charcoal black for app background
top_bar_color = '#800080'  # Purple for the top bar

@ui.refreshable
def chat_messages(own_id):
    # Loop through each message in the messages list
    for user_id, avatar, text, username, timestamp in messages:
        # Determine whether the message is from the current user (sender) or another user (receiver)
        sent_by_own_id = user_id == own_id
        
        # Create a chat message element with different alignment based on the sender
        with ui.chat_message(avatar=avatar, sent=sent_by_own_id):
            # Set the alignment and classes for the chat message
            alignment_class = 'text-left' if sent_by_own_id else 'text-right'
            with ui.row().classes(f'w-full {alignment_class}'):
                # Display the message text and timestamp
                ui.label(f"{username}: {text}").classes('text-white bg-green-500 rounded p-2')
                ui.label(timestamp).classes('text-sm text-gray-400 bg-transparent')

# Define the function to send a message
def send_message(user_id, avatar, text, username):
    # Capture the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Append the new message to the messages list with the user ID, avatar, text, username, and timestamp
    messages.append((user_id, avatar, text.value, username, timestamp))
    # Refresh the chat messages display
    chat_messages.refresh()
    # Clear the text input
    text.value = ''

# Define the chat page
def chat_page(user_id, username, avatar):
    # Create a top bar with the app name and user's name, set the background color to purple
    with ui.row().classes(f'w-full py-2 bg-purple'):
        ui.label('SMART CHAT').classes('text-xl font-bold ml-4 text-white bg-purple')
        ui.label(f'Welcome, {username}').classes('ml-auto mr-4 text-white bg-purple')
    
    # Set up the chat interface with charcoal black background
    with ui.column().classes(f'w-full items-stretch h-full bg-{app_bg_color}'):
        # Display chat messages
        chat_messages(user_id)

    # Footer section with a text input and a send button, also charcoal black
    with ui.footer().classes(f'bg-{app_bg_color} p-2'):
        with ui.row().classes(f'w-full items-center'):
            # Display the user's avatar
            with ui.avatar():
                ui.image(avatar)
            # Create a text input field for sending messages
            text = ui.input(placeholder='Message') \
                .props('rounded outlined').classes('flex-grow bg-white') \
                .on('keydown.enter', lambda: send_message(user_id, avatar, text, username))

# Define the function to prompt for the user's name
def prompt_for_username():
    # Create a text input and button to get the user's name, set the background color to charcoal black
    with ui.column().classes(f'w-full items-center justify-center h-full bg-{app_bg_color}'):
        ui.label('Enter your name:').classes('text-lg text-white')
        name_input = ui.input(placeholder='Your name').props('rounded outlined').classes('flex-grow bg-white')
        # Button to proceed to the chat page with the provided username
        ui.button('Join Chat', on_click=lambda: join_chat(name_input.value)).classes(f'bg-{top_bar_color} text-white')

# Define the function to join the chat
def join_chat(username):
    # Generate a unique user ID
    user_id = str(uuid4())
    # Generate the avatar URL using robohash
    avatar = f'https://robohash.org/{user_id}?bgset=bg2'
    # Redirect to the chat page with the user ID, username, and avatar
    ui.open(f"/chat?user_id={user_id}&username={username}&avatar={avatar}")

# Define the route for the chat page
@ui.page('/chat')
def chat_page_route(user_id, username, avatar):
    chat_page(user_id, username, avatar)

# Define the root page for the application
@ui.page('/')
def index():
    # Prompt for username before entering the chat page
    prompt_for_username()

# Run the NiceGUI application
ui.run()