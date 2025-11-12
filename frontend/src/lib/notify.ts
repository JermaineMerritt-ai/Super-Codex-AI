// src/lib/notify.ts
// Simple notification system for user feedback

export interface NotificationOptions {
  duration?: number; // milliseconds
  type?: 'success' | 'error' | 'warning' | 'info';
}

class NotificationManager {
  private notifications: Map<string, HTMLElement> = new Map();
  private container: HTMLElement | null = null;

  private getContainer(): HTMLElement {
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.id = 'notification-container';
      this.container.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        display: flex;
        flex-direction: column;
        gap: 10px;
        max-width: 400px;
      `;
      document.body.appendChild(this.container);
    }
    return this.container;
  }

  private createNotification(message: string, type: 'success' | 'error' | 'warning' | 'info' = 'info'): HTMLElement {
    const notification = document.createElement('div');
    const id = Math.random().toString(36).substr(2, 9);
    
    const colors = {
      success: { bg: '#4caf50', text: '#fff' },
      error: { bg: '#f44336', text: '#fff' },
      warning: { bg: '#ff9800', text: '#fff' },
      info: { bg: '#2196f3', text: '#fff' }
    };

    notification.style.cssText = `
      background: ${colors[type].bg};
      color: ${colors[type].text};
      padding: 12px 16px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      font-size: 14px;
      line-height: 1.4;
      max-width: 100%;
      word-wrap: break-word;
      animation: slideIn 0.3s ease-out;
    `;

    const closeButton = document.createElement('button');
    closeButton.innerHTML = '×';
    closeButton.style.cssText = `
      background: none;
      border: none;
      color: inherit;
      font-size: 18px;
      cursor: pointer;
      margin-left: 12px;
      padding: 0;
      line-height: 1;
    `;

    closeButton.onclick = () => this.remove(id);

    const messageSpan = document.createElement('span');
    messageSpan.textContent = message;

    notification.appendChild(messageSpan);
    notification.appendChild(closeButton);
    
    this.notifications.set(id, notification);
    return notification;
  }

  private remove(id: string) {
    const notification = this.notifications.get(id);
    if (notification) {
      notification.style.animation = 'slideOut 0.3s ease-in forwards';
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
        this.notifications.delete(id);
      }, 300);
    }
  }

  show(message: string, options: NotificationOptions = {}) {
    const { duration = 5000, type = 'info' } = options;
    const notification = this.createNotification(message, type);
    const container = this.getContainer();
    
    container.appendChild(notification);

    if (duration > 0) {
      setTimeout(() => {
        // Find the ID for this notification element
        let foundId: string | undefined;
        this.notifications.forEach((elem, id) => {
          if (elem === notification) foundId = id;
        });
        if (foundId) this.remove(foundId);
      }, duration);
    }
  }

  success(message: string, duration = 4000) {
    this.show(message, { type: 'success', duration });
  }

  error(message: string, duration = 7000) {
    this.show(message, { type: 'error', duration });
  }

  warning(message: string, duration = 5000) {
    this.show(message, { type: 'warning', duration });
  }

  info(message: string, duration = 5000) {
    this.show(message, { type: 'info', duration });
  }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideOut {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(100%);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);

// Export singleton instance
export const notify = new NotificationManager();