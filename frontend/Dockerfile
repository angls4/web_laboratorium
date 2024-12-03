# Use a Node.js image as the base
FROM node:18 AS build

# Set the working directory in the container
RUN rm -rf /app/staticfiles/*
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) to the container
# COPY package*.json ./
COPY . .

# Install dependencies (including Vite and other project dependencies)
RUN npm install --frozen-lockfile

# Copy the rest of the project files into the container

# Run the Vite build command
RUN npm run build

ENTRYPOINT ["./frontend/entrypoint.sh"]

# The build output will be in the 'dist' folder
# The next step is optional if you just want to access the build output
# You can expose the dist folder as a volume if needed
# VOLUME /app/dist

# Optionally, you can set a default entrypoint for the container, but for build-only, it is not necessary
# ENTRYPOINT ["echo", "Build complete"]
