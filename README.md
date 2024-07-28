
# Livecoding.info

Welcome to [Livecoding.info](https://livecoding.info), a community-driven platform dedicated to showcasing live coding artists from around the world. Our goal is to connect artists and enthusiasts, providing a space to share tools, experiences, and repositories.

## Features

- **Artist Categories**: Browse artists categorized by Audio, Visual, and Other tools.
- **Submit Your Info**: Artists can submit their details using the sidebar form.
- **Download Data**: Easily download the list of artists in CSV format. 

## How to Use

1. **Browse Artists**: Use the tabs to navigate between Audio and Visual live coders. Each category has sub-tabs for specific tools.
2. **Submit Your Info**: If you're an artist, use the sidebar form to submit your details. Select your category, tools, and provide other relevant information.
3. **Download Data**: Download the CSV file containing all artist data directly from the sidebar.

## Contributing

We welcome contributions to improve our data and platform. Here's how you can make a pull request to update the CSV file:

1. **Fork the Repository**: Click the "Fork" button at the top of the repository page to create a copy of the repository on your GitHub account.
2. **Clone Your Fork**: Clone your forked repository to your local machine.
    ```sh
    git clone https://github.com/the-virtual-machine/livecoding.info.git
    ```
3. **Make Changes**: Edit the `info.csv` file with your changes.
4. **Commit Changes**: Commit your changes to your local repository.
    ```sh
    git add info.csv
    git commit -m "Update info.csv with new artist data"
    ```
5. **Push Changes**: Push your changes to your forked repository on GitHub.
    ```sh
    git push origin main
    ```
6. **Create a Pull Request**: Go to the original repository and click the "New Pull Request" button. Compare your forked repository and submit the pull request for review.

## Background
### Tools
- The list for these tools come from [livecode.nyc](https://livecode.nyc/tools) and is not directly affiliated with the group however I would be happy to welcome PRs and collaborate.
- This list of tools can easily be expanded upon, if your tool is not listed in the [Tools](https://github.com/the-virtual-machine/livecoding.info/blob/7d81a6e6742fc61517b77cf6d5b3301dffb99dd4/app.py#L14C1-L18C1)

### Data
- The intended source of truth for data is [this CSV file](/info.csv). Anyone can add data via the form or via a PR and is encouraged to do so.

### Why?
- As the ecosystem and community ofor livecoding expands, it may be helpful to create a tool that helps artists collaborate and for livecoding enthusiasts to find new music and tools

## Contact

If you have any questions or need assistance, please feel free to reach out via a PR or my contact details at [thevirtualmachine.live](https://thevirtualmachine.live/)
