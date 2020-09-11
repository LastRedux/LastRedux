import QtQuick 2.14
import QtQuick.Controls 2.14

import 'Onboarding'

StackView {
  initialItem: connectingPage

  Component {
    id: connectingPage

    OnboardingReady {
      id: welcome
    }
  }
}