[OSV-Scanner](https://google.github.io/osv-scanner/) is offered as a GitHub Action that can be configured to do the following:

1. Trigger a scan with each [pull request](#scan-on-pull-request) and will only report new open source vulnerabilities introduced through the pull request.
2. Perform a full vulnerability scan, configured to run on a [regular schedule](#scheduled-scan).

________
[Scan on pull request](#scan-on-pull-request)

[Scheduled scan](#scheduled-scan)

[Installation](#installation)
- [Automatic Installation](#automatic-installation)
- [Manual Installation](#manual-installation)

[Customization](#customization)

[View results](#view-results)
________

## Scan on pull request
Scanning your project on each pull request can help you keep vulnerabilities out of your project. The pull request scan compares a vulnerability scan of the target branch to a vulnerability scan of the feature branch, and will fail if there are new vulnerabilities introduced through the feature branch. You may choose to [prevent merging](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging) if new vulnerabilities are introduced, but by default the check will only warn users.

## Scheduled scan
Regularly scanning your project for vulnerabilities can alert you to new vulnerabilities in your dependency tree. The scheduled scan will scan your project on a set schedule and report all known vulnerabilities. If vulnerabilities are found the action will return a failed status.

## Installation

The OSV-Scanner GitHub Action can be [automatically](#automatic-installation) or [manually](#manual-installation) installed. 

### Automatic installation

1) From your GitHub project's main page, click “Actions” tab in the navigation bar.

![Select the actions tab on the repository navigation bar.](./images/actions-tab.png)

2) Scroll to the "Security actions" section and click on "View all". This will take you to a url in the form `https://www.github.com/{username}/{repository}/actions/new?category=security` 

![Image indicates the location of the security actions section and the "view all" link.](./images/security-actions.png)

3) Search for "OSV-Scanner". 

![Image shows the GitHub Actions search bar.](./images/actions-tab.png)

4) Choose the "OSV-Scanner" from the list of workflows, and then click “Configure”.

TODO: Insert image

5) Commit the changes.

TODO: Insert image

6) Configure the workflow

The automatically installed GitHub Action includes functionality for both a [scheduled scan](#scheduled-scan) and a [scan on pull request](#scan-on-pull-request). 

If you only want a scheduled scan, you can comment out the "scan-pr" job and only run the action on "schedule" and on "push". 

If you only want to run a scan on pull request, you can comment out the "scan-scheduled" job and only run the action on "pull request" and "merge group". 

If you want both, you can leave the action as is. If you want these functionalities to be seperate for tracking purposes, we recommend following the [manual installation instructions](#manual-installation). 

### Manual installation

To manually install the GitHub Action, please follow instructions on our [main documentation page](https://google.github.io/osv-scanner/github-action/).

## Customization

To learn more about optional inputs for the GitHub Action, please see our [main documentation page](https://google.github.io/osv-scanner/github-action/#customization).

## View results

Maintainers can review results of scheduled scans by navigating to their project's `Security > Code Scanning` tab. Vulnerability details can also be viewed by clicking on the details of the failed action.

For pull request scans, results may be viewed by clicking on the details of the failed action, either from your project's actions tab or directly on the PR. Results are also included in GitHub annotations on the "Files changed" tab for the PR.
