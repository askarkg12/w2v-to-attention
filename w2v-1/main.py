import manim


class StartingScene(manim.Scene):
    def construct(self):
        input_text = manim.Text("Input text")
        input_box = manim.Rectangle(
            width=input_text.width + 0.5, height=input_text.height + 0.5
        )
        input_text.move_to(input_box.get_center())
        input_group = manim.VGroup(input_box, input_text)  # Changed Group to VGroup
        input_group.shift(manim.LEFT * 3)

        output_text = manim.Text("Output text!")
        output_box = manim.Rectangle(
            width=output_text.width + 0.5, height=output_text.height + 0.5
        )
        output_text.move_to(output_box.get_center())
        output_group = manim.VGroup(output_box, output_text)
        output_group.shift(manim.RIGHT * 2)

        arrow = manim.Arrow(
            start=input_group.get_right(), end=output_group.get_left(), buff=0.2
        )

        self.add(input_group)
        self.wait(1)
        self.play(manim.FadeIn(output_group))
        self.wait(1)
        self.play(manim.Create(arrow))
        self.wait(1)

        magic_text = manim.Text("???")  # Using regular text instead of emoji
        magic_box = manim.Rectangle(
            width=magic_text.width + 0.5, height=magic_text.height + 0.5
        )
        magic_text.move_to(magic_box.get_center())
        magic_box = manim.VGroup(magic_box, magic_text)

        # Animate moving input and output groups to align with magic box
        # Calculate new positions first
        input_target = input_group.copy().next_to(magic_box, manim.LEFT, buff=1)
        output_target = output_group.copy().next_to(magic_box, manim.RIGHT, buff=1)

        # Place magic box in center
        magic_box.move_to((input_target.get_right() + output_target.get_left()) / 2)

        # Create two new arrows that will split from the center
        left_arrow = manim.Arrow(
            start=input_target.get_right(), end=magic_box.get_left(), buff=0.2
        )
        right_arrow = manim.Arrow(
            start=magic_box.get_right(), end=output_target.get_left(), buff=0.2
        )

        # Animate everything together
        self.play(
            manim.Transform(input_group, input_target),
            manim.Transform(output_group, output_target),
            manim.ReplacementTransform(arrow, manim.VGroup(left_arrow, right_arrow)),
        )
        self.play(manim.FadeIn(magic_box))
        self.wait(1)


class Word2VecScene(manim.Scene):
    def construct(self):
        input_text = manim.Text("Input text")
        input_box = manim.Rectangle(
            width=input_text.width + 0.5, height=input_text.height + 0.5
        )
        input_text.move_to(input_box.get_center())
        input_group = manim.VGroup(input_box, input_text)  # Changed Group to VGroup

        output_text = manim.Text("Output text!")
        output_box = manim.Rectangle(
            width=output_text.width + 0.5, height=output_text.height + 0.5
        )
        output_text.move_to(output_box.get_center())
        output_group = manim.VGroup(output_box, output_text)

        magic_text = manim.Text("???")  # Using regular text instead of emoji
        magic_box = manim.Rectangle(
            width=magic_text.width + 0.5, height=magic_text.height + 0.5
        )
        magic_text.move_to(magic_box.get_center())
        magic_box = manim.VGroup(magic_box, magic_text)

        input_group.next_to(magic_box, manim.LEFT, buff=1)
        output_group.next_to(magic_box, manim.RIGHT, buff=1)

        arrow1 = manim.Arrow(
            start=input_group.get_right(), end=magic_box.get_left(), buff=0.2
        )
        arrow2 = manim.Arrow(
            start=magic_box.get_right(), end=output_group.get_left(), buff=0.2
        )

        self.add(input_group)
        self.add(output_group)
        self.add(magic_box)
        self.add(arrow1)
        self.add(arrow2)
        self.wait(1)
