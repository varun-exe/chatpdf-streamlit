css = '''
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 1rem; 
}

.chat-message.user {
    background-color: #2b313e;
}

.chat-message.bot {
    background-color: #475063;
}

.chat-message .avatar {
    flex: 0 0 60px; 
    display: flex;
    justify-content: center;
    align-items: center;
}

.chat-message .avatar img {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message .message {
    flex: 1;
    color: #fff;
}
</style>

'''
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://cdn.pixabay.com/photo/2024/03/08/11/35/ai-generated-8620574_1280.png"/>
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://cdn.pixabay.com/photo/2020/06/30/10/23/icon-5355896_1280.png"/>
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
