# HOSI WordPress.com Installation — Current Plan

## $0 public launch

1. Create or open the HOSI site at WordPress.com.
2. Keep the free `*.wordpress.com` address while the project is bootstrapped.
3. Choose a free theme and build with native blocks.
4. Create these pages: Home, About HOSI, Colleges, Courses, Research Library, Founder's Atlas, Policies, Accessibility, Contact.
5. Create `HOSI-101` as a parent course page.
6. Create lesson pages/posts beneath the course index and organize them with categories/tags.
7. Add a course navigation block linking sequential lessons.
8. Add a visible evidence-status block to every lesson.
9. Link GitHub as the canonical curriculum source.
10. Publish only content that has passed the current review gate.

## Plugin/LMS boundary

As of August 2026, WordPress.com plugin installation is available on paid plans, not the free plan. Therefore the $0 MVP should not depend on LearnDash, Tutor LMS, or another plugin. Use native pages/posts/blocks until plugin capability becomes necessary.

WordPress.com also provides a free WordPress.com subdomain on the free plan. A custom domain is a paid-plan feature; annual paid plans can include a one-year domain credit, after which standard renewal pricing applies.

## Upgrade path

When the MVP needs advanced enrollment, quizzes, progress tracking, certificates, drip content, or custom plugin functionality:

1. document the exact requirement;
2. compare available LMS plugins;
3. select the lowest-cost compatible plan;
4. test on staging;
5. migrate published curriculum from GitHub source files;
6. maintain a rollback/export plan.

## Current authoritative WordPress documentation

- https://wordpress.com/free/
- https://wordpress.com/support/plan-features/
- https://wordpress.com/support/plugins/install-a-plugin/
- https://wordpress.com/support/domains/register-a-free-domain/
