import pandas as pd
import random

random.seed(42)

# ==========================================
# SAFE MESSAGE TEMPLATES
# ==========================================

safe_templates = [
    "Please remind me about the meeting at {time}.",
    "The project meeting is scheduled for {time}.",
    "Please send me the notes for today's {subject} class.",
    "Our {event} is happening tomorrow at {time}.",
    "Please bring your {item} for the {activity}.",
    "I will submit the assignment by {time}.",
    "The {activity} has been moved to {time}.",
    "Please check the college notice for the {event}.",
    "Can we discuss the project after {time}?",
    "Your appointment is confirmed for {time}.",
    "The delivery is expected tomorrow.",
    "Please share the meeting link with me.",
    "The workshop starts at {time}.",
    "Remember to bring your ID card.",
    "The exam timetable has been shared.",
    "Please complete the assignment before {time}.",
    "The team discussion will happen after lunch.",
    "I will call you after the class.",
    "The bus will arrive at {time}.",
    "Please send me the project document.",
    "Our presentation is scheduled for Friday.",
    "The lab session starts at {time}.",
    "Can you remind me about the seminar?",
    "The faculty meeting is at {time}.",
    "Please upload the assignment to the portal.",
    "The college event starts at {time}.",
    "I have shared the notes in the group.",
    "The project review is tomorrow.",
    "Please bring the required documents.",
    "The class has been shifted to {time}.",
    "Our team meeting is scheduled for tomorrow.",
    "The library will close at {time}.",
    "Please check the timetable.",
    "The training session starts tomorrow.",
    "I will submit the report today.",
    "The placement workshop is at {time}.",
    "Please confirm your attendance.",
    "The seminar hall is ready.",
    "The assignment deadline is Friday."
]

safe_values = {
    "time": [
        "9 AM", "10 AM", "11 AM", "12 PM",
        "1 PM", "2 PM", "3 PM", "4 PM",
        "5 PM", "6 PM"
    ],
    "subject": [
        "Python", "Java", "Data Structures",
        "Machine Learning", "Database Systems",
        "Computer Networks", "Operating Systems"
    ],
    "event": [
        "workshop", "seminar", "project review",
        "technical event", "college meeting",
        "placement event"
    ],
    "item": [
        "laptop", "ID card", "notebook",
        "project file", "lab record",
        "presentation notes"
    ],
    "activity": [
        "meeting", "workshop", "lab session",
        "seminar", "project review",
        "training", "presentation"
    ]
}


# ==========================================
# SCAM MESSAGE TEMPLATES
# ==========================================

scam_templates = [
    "Congratulations! You have won Rs {amount}. Claim your prize now.",
    "You are selected as a lucky winner. Collect your reward immediately.",
    "Your mobile number has won a cash prize of Rs {amount}.",
    "You have received a special cashback of Rs {amount}. Claim now.",
    "Limited time offer! Get Rs {amount} cashback today.",
    "You have won a free gift voucher worth Rs {amount}.",
    "Congratulations! Your lottery ticket has won Rs {amount}.",
    "Claim your lottery reward before it expires.",
    "You have been selected for a government reward of Rs {amount}.",
    "Your account has received a surprise bonus. Claim it now.",
    "You are eligible for an instant cash reward of Rs {amount}.",
    "Exclusive offer! Get a free gift by paying a small delivery fee.",
    "Your shopping reward is waiting. Claim it immediately.",
    "You have won a smartphone in our lucky draw.",
    "Congratulations! You are today's lucky customer.",
    "Get guaranteed profit from this special investment opportunity.",
    "Invest Rs {amount} today and receive huge returns.",
    "Earn money quickly from our work from home opportunity.",
    "You have been selected for a high salary part-time job.",
    "Pay a small registration fee to receive your job offer.",
    "Your refund of Rs {amount} is ready. Claim immediately.",
    "You are eligible for a special loan with zero processing fee.",
    "Get an instant loan approved today. Apply immediately.",
    "Your delivery requires a small payment to receive the package.",
    "Pay the delivery charge now to receive your gift.",
    "Your insurance bonus is ready. Claim your money today.",
    "Congratulations! Your lucky coupon has won Rs {amount}.",
    "Your recharge account has received a bonus reward.",
    "You have been chosen for a special promotional prize.",
    "Claim your free holiday package before the offer expires.",
    "You won a shopping voucher. Redeem it immediately.",
    "Your exclusive reward is waiting for you.",
    "Receive double cashback if you complete the payment today.",
    "Special investment scheme guarantees huge returns.",
    "You have won an expensive electronic gift.",
    "Pay Rs {amount} to unlock your reward.",
    "Your prize cannot be delivered until you pay the fee."
]

scam_values = {
    "amount": [
        "1000", "2500", "5000", "7500",
        "10000", "15000", "25000",
        "50000", "75000", "100000",
        "200000", "500000"
    ]
}


# ==========================================
# PHISHING MESSAGE TEMPLATES
# ==========================================

phishing_templates = [
    "Your bank account needs immediate verification.",
    "Your bank account will be blocked unless you verify your details.",
    "Please verify your banking information to avoid account suspension.",
    "Your KYC verification is pending. Complete it immediately.",
    "Your KYC has expired. Update your details now.",
    "Your bank card will be blocked. Verify your account.",
    "Your debit card requires security verification.",
    "Your credit card has been temporarily suspended.",
    "Confirm your bank login to restore access.",
    "Your internet banking access requires verification.",
    "Your account security check is pending.",
    "Verify your account password to continue.",
    "Your login session has expired. Sign in again.",
    "Confirm your username and password immediately.",
    "Your account has detected unusual activity.",
    "Verify your identity to secure your account.",
    "Your OTP verification is required to continue.",
    "Enter the OTP received on your phone.",
    "Your payment could not be completed. Verify your card.",
    "Confirm your card details to complete the payment.",
    "Your UPI account requires verification.",
    "Verify your UPI PIN to restore your account.",
    "Your wallet account has been suspended.",
    "Confirm your payment information immediately.",
    "Your account will be permanently locked.",
    "Security verification is required for your account.",
    "Your password must be verified immediately.",
    "Your banking profile needs an urgent security update.",
    "Confirm your identity before accessing your account.",
    "Your account has been flagged for suspicious activity.",
    "Verify your card number and security information.",
    "Your online banking account needs immediate verification.",
    "Your account access has been restricted.",
    "Update your security information to avoid suspension.",
    "Your payment account requires identity verification.",
    "Confirm your login details to continue using the service.",
    "Your account security settings need confirmation.",
    "Verify your registered mobile number immediately.",
    "Your bank service requires a security confirmation.",
    "Your account verification deadline is today."
]


# ==========================================
# FUNCTION TO CREATE VARIATIONS
# ==========================================

def create_variations(templates, values, target_count):
    messages = set()

    extra_phrases = [
        "",
        " Please act now.",
        " Complete this today.",
        " Do this immediately.",
        " Please respond soon.",
        " Take action today.",
        " Follow the instructions carefully.",
        " Please check this now.",
        " This is important.",
        " Kindly complete the request."
    ]

    while len(messages) < target_count:

        template = random.choice(templates)

        message = template

        for key, options in values.items():

            placeholder = "{" + key + "}"

            if placeholder in message:
                message = message.replace(
                    placeholder,
                    random.choice(options)
                )

        message = message + random.choice(extra_phrases)

        messages.add(message)

    return list(messages)


# ==========================================
# CREATE DATA
# ==========================================

safe_messages = create_variations(
    safe_templates,
    safe_values,
    130
)

scam_messages = create_variations(
    scam_templates,
    scam_values,
    130
)

phishing_messages = create_variations(
    phishing_templates,
    {},
    130
)


# ==========================================
# COMBINE DATA
# ==========================================

data = []

for message in safe_messages:
    data.append([message, "safe"])

for message in scam_messages:
    data.append([message, "scam"])

for message in phishing_messages:
    data.append([message, "phishing"])


random.shuffle(data)


# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(
    data,
    columns=["message", "label"]
)


# ==========================================
# SAVE DATASET
# ==========================================

output_file = "datasets/messages_review2_diverse_390.csv"

df.to_csv(
    output_file,
    index=False
)


# ==========================================
# DISPLAY RESULT
# ==========================================

print()
print("======================================")
print(" REVIEW 2 DATASET CREATED SUCCESSFULLY")
print("======================================")
print("Total messages :", len(df))
print("Safe messages  :", len(df[df["label"] == "safe"]))
print("Scam messages  :", len(df[df["label"] == "scam"]))
print("Phishing       :", len(df[df["label"] == "phishing"]))
print("Saved file     :", output_file)
print("======================================")