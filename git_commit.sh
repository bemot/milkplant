#!/bin/bash

# Git Commit Script for Yogurt Production Optimizer
# Usage: ./git_commit.sh "Your commit message"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if commit message is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Commit message required${NC}"
    echo "Usage: ./git_commit.sh \"Your commit message\""
    exit 1
fi

COMMIT_MESSAGE="$1"

echo -e "${YELLOW}Checking git status...${NC}"
git status

echo ""
echo -e "${YELLOW}Adding all changes...${NC}"
git add .

echo ""
echo -e "${YELLOW}Current staged changes:${NC}"
git status --short

echo ""
read -p "Do you want to commit these changes? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Committing changes...${NC}"
    git commit -m "$COMMIT_MESSAGE"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Successfully committed changes!${NC}"
        echo ""
        echo -e "${YELLOW}Recent commits:${NC}"
        git log --oneline -5
        echo ""
        echo -e "${YELLOW}To push to GitHub, run:${NC}"
        echo "git push origin main"
    else
        echo -e "${RED}Commit failed!${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}Commit cancelled.${NC}"
    exit 0
fi
