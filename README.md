# Bug/Issue Tracker App

### Table of Contents

- Introduction
- Features
- Getting Started
  - Prerequisites
  - Installation
- Usage
  - Creating a New Issue
  - Managing Issues
- Contributing
- License

### Introduction

The Bug/Issue Tracker App is a web-based application designed to help teams and organizations efficiently track and manage software bugs, issues, feature requests, and tasks. It provides a centralized platform for capturing, prioritizing, and resolving issues, ensuring that teams can collaborate effectively to deliver high-quality software.

### Features

- Issue Creation: Users can easily create new issues, providing detailed information about the problem, its severity, and any necessary attachments like screenshots or code snippets.

- Issue Tracking: The app allows users to track the status and progress of each issue, from creation to resolution. Common issue statuses include Open, In Progress, Resolved, Closed, and more.

- Assigning and Prioritizing: Issues can be assigned to specific team members and prioritized based on their urgency and impact on the project.

- Commenting and Collaboration: Team members can leave comments and collaborate within each issue, facilitating communication and providing a clear audit trail of discussions.

- Search and Filtering: Users can easily search for specific issues and apply filters to view a subset of issues based on criteria like status, priority, or assignee.

### Getting Started

#### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python >=3.10
- Poetry

#### Installation

1. Clone repo
   `git clone https://github.com/ademolab91/bugtracker-app.git`
   `cd bugtracker-app`
2. Install dependencies
   `poetry install`
3. Activate virtual env
   `poetry shell`
4. Populate database
   `python bugtracker_app/examples.py`
5. Run app
   `reflex run`

### Contributing

I welcome contributions from the community! To contribute to the Bug/Issue Tracker App, follow these steps:

1. Fork the repository on GitHub.

2. Clone your forked repository to your local machine.

3. Create a new branch for your feature or bug fix.

4. Make your changes and commit them with clear and concise commit messages.

5. Push your changes to your forked repository on GitHub.

6. Create a pull request to the main repository, explaining your changes and the problem they solve.

I will review your pull request and provide feedback. Thank you for contributing!

### License

This project is licensed under the [MIT License](https://opensource.org/license/mit/).
