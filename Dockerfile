FROM python:3.10-slim

# Install Tkinter and other system packages
RUN apt-get update && \
    apt-get install -y python3-tk x11-apps && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Set display so it connects to host's X11
ENV DISPLAY=:0

# Run the app
CMD ["python", "main.py"]
