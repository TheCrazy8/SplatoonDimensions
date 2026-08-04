---
title: Team
---

# Meet the Team

The people behind BrightOS and the Blaze robotics framework.

[[TOC]]

## Core Team

<div class="team-grid">
  <div class="team-card">
    <div class="team-avatar">
      <img src="https://github.com/TheCrazy8.png" alt="TheCrazy8" />
    </div>
    <div class="team-info">
      <h3>TheCrazy8</h3>
      <p class="team-role">Founder & Lead Developer</p>
      <p class="team-bio">Creator of BrightOS and the Blaze robotics framework. Passionate about making robotics accessible to everyone.</p>
      <div class="team-links">
        <a href="https://github.com/TheCrazy8" target="_blank" rel="noopener noreferrer">GitHub</a>
      </div>
    </div>
  </div>
  <div class="team-card">
    <div class="team-avatar">
      <img src="https://avatars.githubusercontent.com/u/186629374?v=4" alt="Pumpjack" />
    </div>
    <div class="team-info">
      <h3>Pumpjack</h3>
      <p class="team-role">Cofounder & Lead Developer</p>
      <p class="team-bio">TheCrazy8's partner in crime, and original coder for Blaze before the transition from VEX to a custom framework.</p>
      <div class="team-links">
        <a href="https://github.com/C937-IT-A" target="_blank" rel="noopener noreferrer">GitHub</a>
      </div>
    </div>
  </div>
</div>

## How to Join

We're always looking for contributors! Here's how you can get involved:

### 🛠️ Code Contributions
- Fork the [repository](https://github.com/TheCrazy8/Blaze-Official)
- Fix bugs or implement features
- Submit pull requests
- Review code from other contributors

### 📖 Documentation
- Improve existing docs
- Write tutorials and guides
- Translate documentation
- Report documentation issues

### 🎨 Design
- Create UI improvements
- Design icons and graphics
- Improve site accessibility
- Suggest UX enhancements

### 🧪 Testing
- Report bugs with detailed steps
- Test on different platforms
- Verify plugin compatibility
- Performance testing

### 💬 Community
- Answer questions on [GitHub Discussions](https://github.com/TheCrazy8/Blaze-Official/discussions)
- Share your BrightOS projects
- Write blog posts about your experience
- Help newcomers get started

## Contributors

::: info Open Source Community
BrightOS thrives thanks to contributions from the community. Every contribution, no matter how small, makes a difference!

Want to see your name here? [Start contributing today!](https://github.com/TheCrazy8/Blaze-Official)
:::

---

**Interested in joining the team?** Reach out on [GitHub Discussions](https://github.com/TheCrazy8/Blaze-Official/discussions) or start contributing to the project!

<style scoped>
.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin: 24px 0;
}

.team-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 24px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 16px;
  background: var(--vp-c-bg-soft);
  transition: all 0.3s ease;
  text-align: center;
}

.team-card:hover {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 8px 24px rgba(255, 69, 0, 0.15);
  transform: translateY(-4px);
}

.team-avatar {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 16px;
  border: 3px solid var(--vp-c-brand-1);
  box-shadow: 0 0 16px rgba(255, 69, 0, 0.2);
}

.team-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.team-info h3 {
  margin: 0 0 4px;
  font-size: 20px;
  font-weight: 700;
  color: var(--vp-c-text-1);
}

.team-role {
  margin: 0 0 12px;
  font-size: 14px;
  font-weight: 600;
  color: var(--vp-c-brand-1);
}

.team-bio {
  margin: 0 0 16px;
  font-size: 14px;
  color: var(--vp-c-text-2);
  line-height: 1.6;
}

.team-links {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.team-links a {
  padding: 6px 16px;
  border: 1px solid var(--vp-c-brand-1);
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  color: var(--vp-c-brand-1);
  text-decoration: none;
  transition: all 0.2s;
}

.team-links a:hover {
  background: var(--vp-c-brand-1);
  color: white;
}

@media (max-width: 640px) {
  .team-grid {
    grid-template-columns: 1fr;
  }
}
</style>
