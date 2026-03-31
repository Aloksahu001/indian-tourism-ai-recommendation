def get_reply(msg):
    msg = msg.lower()
    if "beach" in msg:
        return "You can visit Goa, Varkala, Baga Beach"
    if "hill" in msg:
        return "Manali, Ooty, Munnar are good hill stations"
    if "religious" in msg:
        return "Varanasi, Tirupati, Amritsar are famous"
    return "Please ask about hill, beach, religious tourism"
