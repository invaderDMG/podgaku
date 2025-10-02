# Contributing to Podgaku Podcast RSS Generator

Thank you for your interest in contributing to this project! 🎉

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/podcastXMLgen.git
   cd podcastXMLgen
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Create a `.env` file** from the example:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

## 🛠️ Development Setup

### Local Development
```bash
# Start the web server
python start_web.py

# Run tests (if available)
python -m pytest

# Check code style
flake8 *.py
```

### Testing Your Changes
1. Test the web interface at `http://localhost:8080`
2. Try adding a sample episode
3. Verify RSS generation works
4. Test SFTP upload (with test credentials)

## 📝 How to Contribute

### Reporting Bugs
1. **Check existing issues** first
2. **Create a detailed bug report** with:
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Error messages or logs

### Suggesting Features
1. **Open an issue** with the "enhancement" label
2. **Describe the feature** and its use case
3. **Explain why** it would be valuable

### Code Contributions

#### Before You Start
- **Check existing issues** for similar work
- **Open an issue** to discuss major changes
- **Keep changes focused** - one feature per PR

#### Coding Standards
- **Follow PEP 8** Python style guide
- **Use meaningful variable names**
- **Add comments** for complex logic
- **Write docstrings** for functions and classes
- **Keep functions small** and focused

#### Example Code Style
```python
def generate_rss_item(episode: Episode) -> ET.Element:
    """
    Generate RSS item element for a podcast episode.
    
    Args:
        episode: Episode object with metadata
        
    Returns:
        XML Element representing the RSS item
    """
    item = ET.Element("item")
    # ... implementation
    return item
```

#### Pull Request Process
1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** with clear commits
3. **Test thoroughly**
4. **Update documentation** if needed
5. **Submit a pull request** with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots (for UI changes)

## 🎯 Areas for Contribution

### High Priority
- [ ] **Unit tests** for core functionality
- [ ] **Integration tests** for SFTP deployment
- [ ] **Error handling** improvements
- [ ] **Performance optimizations**

### Medium Priority
- [ ] **Additional audio formats** support
- [ ] **Batch episode upload** feature
- [ ] **RSS validation** tools
- [ ] **Theme customization** options

### Low Priority
- [ ] **Multi-language support**
- [ ] **Database backend** option
- [ ] **API endpoints** for external tools
- [ ] **Advanced analytics**

## 🔧 Technical Guidelines

### File Structure
- **Core logic**: `podcast_manager.py`, `episode_manager.py`, `rss_generator.py`
- **Web interface**: `web_server.py`, `templates/`, `static/`
- **Deployment**: `sftp_uploader.py`, `deploy_to_ftp.py`
- **Configuration**: `podcast_config.py`, `.env`

### Adding New Features
1. **Update relevant core modules**
2. **Add web interface** if needed
3. **Update configuration** options
4. **Add documentation**
5. **Update CHANGELOG.md**

### Database Changes
- **Backup compatibility**: Ensure `episodes.json` format remains compatible
- **Migration scripts**: Provide upgrade paths for existing users
- **Documentation**: Update README with new requirements

## 🧪 Testing

### Manual Testing Checklist
- [ ] Web interface loads correctly
- [ ] File upload works with MP3/M4A
- [ ] Metadata extraction functions
- [ ] RSS generation produces valid XML
- [ ] SFTP deployment succeeds
- [ ] Static web frontend displays correctly

### Automated Testing (Future)
We welcome contributions to add:
- Unit tests for core functions
- Integration tests for deployment
- RSS validation tests
- Web interface tests

## 📚 Documentation

### When to Update Documentation
- **New features** - Update README and relevant docs
- **Configuration changes** - Update examples and guides
- **Bug fixes** - Update troubleshooting section
- **API changes** - Update function documentation

### Documentation Style
- **Clear and concise** explanations
- **Step-by-step** instructions
- **Code examples** for complex features
- **Screenshots** for UI changes

## 🎉 Recognition

Contributors will be:
- **Listed in CONTRIBUTORS.md**
- **Mentioned in release notes**
- **Credited in commit messages**

## 📞 Getting Help

- **GitHub Issues** - For bugs and feature requests
- **GitHub Discussions** - For questions and ideas
- **Email** - For security issues or private matters

## 🏷️ Versioning

We use [Semantic Versioning](https://semver.org/):
- **MAJOR** - Breaking changes
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make this project better! 🚀**
