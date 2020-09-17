import QtQuick 2.14
import QtQuick.Controls 2.14

import 'Onboarding'

StackView {
  initialItem: welcomePage

  Component {
    id: welcomePage

    OnboardingWelcome {
      id: welcome
    }
  }
}